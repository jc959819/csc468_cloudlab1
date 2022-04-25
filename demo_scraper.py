import scraper

def main():
	# Get product details for top selling GPUs
	product_details = scraper.get_best_selling_gpus()
	
	# Print key, value pairs line by line
	for key, value in product_details.items():
		print(key, ":", value)

if __name__ == "__main__":
	main()
