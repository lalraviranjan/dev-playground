def search_products(
    category: str,
    budget: str = None,
    brand: str = None
) -> str:

    print("category =", category)
    print("budget =", budget)
    print("brand =", brand)

    products = [

        {
            "name": "Dell XPS 13",
            "category": "laptop",
            "brand": "Dell",
            "price": 95000
        },

        {
            "name": "MacBook Air M2",
            "category": "laptop",
            "brand": "Apple",
            "price": 110000
        },

        {
            "name": "HP Pavilion 15",
            "category": "laptop",
            "brand": "HP",
            "price": 70000
        },

        {
            "name": "Lenovo Legion 5",
            "category": "laptop",
            "brand": "Lenovo",
            "price": 98000
        }
    ]

    category = category.lower()

    filtered = [
        p for p in products
        if p["category"].lower() in category
        or category in p["category"].lower()
    ]

    if brand:

        filtered = [
            p for p in filtered
            if p["brand"].lower() == brand.lower()
        ]

    if not filtered:
        return "No products found matching your criteria."

    result = "Recommended Products:\n\n"

    for p in filtered:

        result += (
            f"• {p['name']} "
            f"({p['brand']}) - ₹{p['price']}\n"
        )

    return result