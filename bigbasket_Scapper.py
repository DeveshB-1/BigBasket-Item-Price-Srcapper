import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

def extract_quantity(text):
    """
    Extract quantity information from text with broader pattern coverage.
    """
    pattern = r'(\b\d+\s*(?:g|gm|gms|kg|kgs|litre|ltr|ml|count|piece|pc|pack|pouch|tin|bottle|carton|bag|dozen)\b)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else ""

def search_products(ingredient):
    """
    Searches Bigbasket for the given ingredient.
    Constructs a search URL and iterates over anchor tags with href containing "/pd/".
    Extracts the product name and price and ensures every word in the query appears in the product name.
    """
    search_url = f"https://www.bigbasket.com/ps/?q={ingredient}"

    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    query_words = ingredient.lower().split()

    for a in soup.find_all("a", href=True):
        if "/pd/" in a["href"]:
            product_name = a.get_text(separator=" ", strip=True)

            if not all(word in product_name.lower() for word in query_words):
                continue

            quantity = extract_quantity(product_name)

            # Check if quantity isn't found in the name; try neighboring elements
            if not quantity:
                quantity_element = a.find_next("span", string=re.compile(r'\d+\s*(?:g|kg|ml|ltr|piece|pack|pouch)', re.IGNORECASE))
                if quantity_element:
                    quantity = quantity_element.get_text(strip=True)

            price_div = a.find_next("div", class_=lambda x: x and "Pricing___StyledDiv" in x)
            price = None

            if price_div:
                price_span = price_div.find("span", class_=lambda x: x and "Pricing___StyledLabel" in x)
                if price_span:
                    price = price_span.get_text(strip=True)

            if product_name and price:
                products.append({
                    "name": product_name,
                    "price": price,
                    "quantity": quantity
                })
                break

    return products

def save_result_to_excel(result, filename='bigbasket_data.xlsx'):
    """
    Saves a single product result to an Excel file.
    Appends to the file if it exists; otherwise, creates a new one.
    """
    new_data = pd.DataFrame([result])

    if os.path.exists(filename):
        try:
            df = pd.read_excel(filename)
            df = pd.concat([df, new_data], ignore_index=True)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            df = new_data
    else:
        df = new_data

    try:
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error writing to Excel: {e}")

@app.route('/api/ingredient', methods=['GET'])
def ingredient_api():
    """
    API endpoint to search for an ingredient on Bigbasket.
    Example usage: /api/ingredient?name=green apple
    Returns only the first matching product (with name, price, and quantity) and saves it to Excel.
    """
    ingredient = request.args.get('name')

    if not ingredient:
        return jsonify({
            "error": "Please provide an ingredient name using the 'name' query parameter."
        }), 400

    results = search_products(ingredient)

    if not results:
        return jsonify({
            "error": f"No products found for '{ingredient}'"
        }), 404

    single_result = results[0]
    save_result_to_excel(single_result)
    return jsonify(single_result), 200

if __name__ == '__main__':
    app.run(debug=True)