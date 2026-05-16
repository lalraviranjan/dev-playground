def get_product_details(product_name: str) -> str:

    mock_db = {

        "Dell XPS 13": {
            "processor": "Intel i7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "weight": "1.2kg",
            "battery": "12 hours",
            "display": "13.4-inch FHD+",
            "os": "Windows 11",
            "price": "₹95,000"
        },

        "MacBook Air M2": {
            "processor": "Apple M2",
            "ram": "16GB",
            "storage": "512GB SSD",
            "weight": "1.24kg",
            "battery": "18 hours",
            "display": "13.6-inch Liquid Retina",
            "os": "macOS",
            "price": "₹1,10,000"
        }
    }

    product = mock_db.get(product_name)

    if not product:
        return "Product details not found."

    return (
        f"{product_name} Specifications:\n\n"
        f"• Processor: {product['processor']}\n"
        f"• RAM: {product['ram']}\n"
        f"• Storage: {product['storage']}\n"
        f"• Weight: {product['weight']}\n"
        f"• Battery: {product['battery']}\n"
        f"• Display: {product['display']}\n"
        f"• OS: {product['os']}\n"
        f"• Price: {product['price']}"
    )