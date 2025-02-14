# BigBasket Item Price Scraper

This project is a web scraper for extracting product names, prices, and quantities from BigBasket's website. It uses Python, Beautiful Soup, and Flask to provide a simple API interface for fetching product details.

## Features
- Search for products by name.
- Extract product name, price, and quantity.
- Save results to an Excel file.
- Lightweight Flask-based API.

## Technologies Used
- Python
- Flask
- Beautiful Soup
- Requests
- Pandas

## Installation

1. Clone the repository:
```bash
git clone git@github.com:DeveshB-1/BigBasket-Item-Price-Srcapper.git
cd BigBasket-Item-Price-Srcapper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Create a `requirements.txt` file with:**
```plaintext
flask
beautifulsoup4
pandas
requests
openpyxl
```

## Usage

1. Run the Flask server:
```bash
python bigbasket_scraper.py
```

2. Access the API:
```bash
http://localhost:5000/api/ingredient?name=apple
```

The result will include the product name, price, and quantity, and the data will be saved to `bigbasket_data.xlsx`.

## Example Response
```json
{
  "name": "Fresho Apple - Shimla, Regular",
  "price": "₹286",
  "quantity": "500 g"
}
```

## Notes
- This scraper relies on the BigBasket website's current structure and may break if the site layout changes.
- Use responsibly and follow web scraping best practices.

