from strands.tools import tool
from ddgs.exceptions import DDGSException, RatelimitException
from ddgs import DDGS
from strands_tools import retrieve
import boto3

# MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
MODEL_ID = "amazon.nova-micro-v1:0"

# System prompt defining the agent's role and capabilities
SYSTEM_PROMPT = """You are a smart and personalized shopping assistant for an e-commerce platform.

Your role is to:
- Understand user shopping needs such as product type, budget, brand, and usage
- Remember user preferences and use them automatically in future recommendations
- Provide relevant product suggestions using available tools
- Ask clarifying questions if requirements are unclear
- Be friendly, concise, and helpful in all interactions
- Continuously improve recommendations based on past interactions

You have access to the following tools:
1. search_products() - To find products based on category, budget, and brand
2. get_product_details() - To provide detailed specifications of a product
3. compare_products() - To compare multiple products
4. save_user_preference() - To store user preferences for future use

Always use the appropriate tool to provide accurate and personalized recommendations instead of making assumptions."""

@tool
def search_products(category: str, budget: str = None, brand: str = None) -> str:
    """
    Search for products based on category, budget, and brand preferences.
    """

    print("category =", category)
    print("budget =", budget)
    print("brand =", brand)

    # Mock product catalog
    products = [
        {"name": "Dell XPS 13", "category": "laptop", "brand": "Dell", "price": 95000},
        {"name": "MacBook Air M2", "category": "laptop", "brand": "Apple", "price": 110000},
        {"name": "HP Pavilion 15", "category": "laptop", "brand": "HP", "price": 70000},
        {"name": "Lenovo Legion 5", "category": "laptop", "brand": "Lenovo", "price": 98000},
    ]

    # Normalize input
    category = category.lower()

    # Flexible category matching
    filtered = [
        p for p in products
        if p["category"].lower() in category
        or category in p["category"].lower()
    ]

    # Brand filtering
    if brand:
        filtered = [
            p for p in filtered
            if p["brand"].lower() == brand.lower()
        ]

    # Budget filtering
    if budget:
        try:
            min_b, max_b = map(int, budget.split("-"))

            filtered = [
                p for p in filtered
                if min_b <= p["price"] <= max_b
            ]

        except Exception:
            print("Invalid budget format")

    print("DEBUG FILTERED =", filtered)

    if not filtered:
        return "No products found matching your criteria."

    result = "Recommended Products:\n\n"

    for p in filtered:
        result += (
            f"• {p['name']} ({p['brand']}) - ₹{p['price']}\n"
        )

    return result

@tool
def get_product_details(product_name: str) -> str:
    """
    Get detailed specifications of a product.

    Args:
        product_name: Name of the product

    Returns:
        Product specifications and features
    """

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
        },

        "HP Pavilion 15": {
            "processor": "Intel i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "weight": "1.75kg",
            "battery": "8 hours",
            "display": "15.6-inch FHD",
            "os": "Windows 11",
            "price": "₹70,000"
        },

        "Lenovo Legion 5": {
            "processor": "AMD Ryzen 7",
            "ram": "16GB",
            "storage": "1TB SSD",
            "weight": "2.4kg",
            "battery": "6 hours",
            "display": "15.6-inch 165Hz",
            "os": "Windows 11",
            "gpu": "NVIDIA RTX 4060",
            "price": "₹98,000"
        },

        "Lenovo ThinkPad E14": {
            "processor": "Intel i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "weight": "1.59kg",
            "battery": "10 hours",
            "display": "14-inch FHD",
            "os": "Ubuntu / Windows 11",
            "price": "₹82,000"
        },

        "ASUS TUF Gaming F15": {
            "processor": "Intel i7",
            "ram": "16GB",
            "storage": "1TB SSD",
            "weight": "2.2kg",
            "battery": "7 hours",
            "display": "15.6-inch 144Hz",
            "os": "Windows 11",
            "gpu": "NVIDIA RTX 4050",
            "price": "₹92,000"
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
        f"• Battery: {product['battery']}"
    )
    
@tool
def compare_products(product1: str, product2: str) -> str:
    """
    Compare two products.

    Args:
        product1: First product
        product2: Second product

    Returns:
        Comparison summary
    """

    return (
        f"Comparison:\n\n"
        f"{product1} vs {product2}\n\n"
        f"• Performance: Comparable\n"
        f"• Battery: {product2} slightly better\n"
        f"• Price: {product1} more affordable\n"
        f"• Recommendation: Choose based on OS preference"
    )

print("✅ Product comparison tool ready")
