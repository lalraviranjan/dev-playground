from search_products import search_products
from get_product_details import get_product_details
from compare_products import compare_products


def get_named_parameter(event, name):
    """
    Safely fetch named parameter from MCP event.
    """

    if name not in event:
        return None

    return event.get(name)


def lambda_handler(event, context):

    print(f"Event: {event}")
    print(f"Context: {context}")

    # =====================================================
    # MCP TOOL NAME
    # =====================================================

    extended_tool_name = (
        context.client_context.custom["bedrockAgentCoreToolName"]
    )

    resource = extended_tool_name.split("___")[1]

    print(f"Invoked Tool: {resource}")

    # =====================================================
    # SEARCH PRODUCTS
    # =====================================================

    if resource == "search_products":

        category = get_named_parameter(
            event=event,
            name="category"
        )

        budget = get_named_parameter(
            event=event,
            name="budget"
        )

        brand = get_named_parameter(
            event=event,
            name="brand"
        )

        if not category:
            return {
                "statusCode": 400,
                "body": "❌ Please provide category"
            }

        try:

            result = search_products(
                category=category,
                budget=budget,
                brand=brand
            )

        except Exception as e:

            print(e)

            return {
                "statusCode": 500,
                "body": f"❌ {str(e)}"
            }

        return {
            "statusCode": 200,
            "body": result
        }

    # =====================================================
    # GET PRODUCT DETAILS
    # =====================================================

    elif resource == "get_product_details":

        product_name = get_named_parameter(
            event=event,
            name="product_name"
        )

        if not product_name:
            return {
                "statusCode": 400,
                "body": "❌ Please provide product_name"
            }

        try:

            result = get_product_details(
                product_name=product_name
            )

        except Exception as e:

            print(e)

            return {
                "statusCode": 500,
                "body": f"❌ {str(e)}"
            }

        return {
            "statusCode": 200,
            "body": result
        }

    # =====================================================
    # COMPARE PRODUCTS
    # =====================================================

    elif resource == "compare_products":

        product1 = get_named_parameter(
            event=event,
            name="product1"
        )

        product2 = get_named_parameter(
            event=event,
            name="product2"
        )

        if not product1 or not product2:
            return {
                "statusCode": 400,
                "body": "❌ Please provide product1 and product2"
            }

        try:

            result = compare_products(
                product1=product1,
                product2=product2
            )

        except Exception as e:

            print(e)

            return {
                "statusCode": 500,
                "body": f"❌ {str(e)}"
            }

        return {
            "statusCode": 200,
            "body": result
        }

    # =====================================================
    # UNKNOWN TOOL
    # =====================================================

    return {
        "statusCode": 400,
        "body": f"❌ Unknown toolname: {resource}"
    }