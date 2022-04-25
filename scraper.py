# Author(s): 	Shaun Derstine
# Last Edit: 	4/19/2022 
# Description: 	This program contains function(s) for retreiving the item name, price,
#		and as-of date of a product listed on newegg

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from sys import argv
from datetime import date

# Input:	url
# Output: 	bs4 object
def convert_url(url):
	# urlopen makes a request to webpage at url
	# result is an object which is saved as url_object
	url_object = urlopen(url)

	# the raw html from the webpage is saved in html_doc
	html_doc = url_object.read()

	# converts raw html to BeautifulSoup object 'soup'
	soup = bs(html_doc, "html.parser")

	return soup
# end convert_url()

# Input:	url to product page
# Output:	dictionary holding product details from given link
# Format:	{ "item":"", "price":"", "date":"" }
def get_product(url):
	# convert url into bs4 object
	soup = convert_url(url)

	# PRODUCT TITLE
	item_name = soup.find("h1", class_="product-title").string

	# CURRENT PRICE
	li_elem = soup.find("li", class_="price-current")

	# starting from index 1 in the children of the li element,
	# $, dollar amount, cent amount
	cur_price = ""
	for i in range(1, len(li_elem.contents)):
		# concat each segment of current price to string
		cur_price += li_elem.contents[i].string

	# CURRENT DATE (yyyy-mm-dd)
	cur_date = date.today().isoformat()

	# return as dictionary
	return { "item":item_name, "price":cur_price, "date":cur_date }
# end get_product()

# Input:	None
# Output:	Dictionary containing product details for top 36 best selling GPUs on Newegg
# Format:	{ "item":[""], "price":[""], "date":[""] }
def get_best_selling_gpus():
	# Convert webpage listing best selling GPUs into bs object
	link_to_best_selling_page = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709&Order=3"
	soup = convert_url(link_to_best_selling_page)

	# Make something to hold GPU details
	# Dictionary, list, store directly in database??

	# Get all GPUs listed on page into list
	gpus = soup.find_all("a", class_="item-title")

	# Dictionary to hold product details
	product_details = {
		"items":[],
		"prices":[],
		"dates":[]
	}

	# Get product details for each GPU
	for gpu in gpus:
		details = get_product(gpu["href"])
		product_details["items"].append(details["item"])
		product_details["prices"].append(details["price"])
		product_details["dates"].append(details["date"])

	return product_details
# end get_best_selling_gpus()
