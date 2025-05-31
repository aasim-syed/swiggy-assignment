import json  # For loading and parsing the product database from a JSON file
import os    # For constructing file paths in a cross-platform way
from agents.user_clarifier import clarify_preferences  # Function to re-prompt user for preferences
from agents.image_analyzer import analyze_image      # Function to analyze a new image if needed

def recommend_product(context):
    """
    TODO:
    Recommend products based on user preferences and/or detected product type.
    Updates the context with matching recommendations or triggers follow-up steps.
    """
    # Retrieve stored user preferences (brand, color, price, etc.) from context
    preferences = context.get("preferences", {})
    # Determine product type (e.g., "electronics" or "sneakers") from context; default to generic "product"
    product_type = context.get("product_type", "product").lower()

    # Extract individual preference fields, defaulting to "any" if not specified
    brand = preferences.get("brand", "any").lower()
    color = preferences.get("color", "any").lower()
    # Price range string might be something like "1000-5000". Default to "0-100000" if missing.
    price_range = preferences.get("price_range", "0-100000").strip()
    # Category preference, or fallback to the detected product_type
    category = preferences.get("category", "").lower() or product_type

    # Parse the price_range string into numeric min_price and max_price
    try:
        if "-" in price_range:
            # Split on hyphen to get min and max as integers
            min_price, max_price = map(int, price_range.split("-"))
        else:
            # If no hyphen, interpret the entire string as the upper limit
            min_price = 0
            max_price = int(price_range)
    except:
        # If parsing fails, fall back to a very broad price range
        min_price, max_price = 0, float("inf")

    # Construct the path to the mock_products.json file
    json_path = os.path.join(
        os.path.dirname(__file__),    # Directory where this script resides
        "..",                          # Go up one level
        "product_db",                  # Enter the product_db folder
        "mock_products.json"           # File containing the product catalog
    )
    # Load the product catalog from the JSON file
    with open(json_path, "r") as f:
        product_catalog = json.load(f)

    def match(product):
        """
        Helper function to check if a given product matches the user's criteria.
        Returns True if the product should be included, False otherwise.
        """
        # Normalize product fields for comparison
        p_brand = product.get("brand", "").lower()
        p_color = product.get("color", "").lower()
        p_price = product.get("price", 0)
        p_category = product.get("category", "").lower()

        # Check category match (either direction—user category in product category or vice versa),
        # brand match (or "any"), color match (or "any"), and price within the specified range.
        return (
            (category in p_category or p_category in category)
            and (brand == "any" or brand in p_brand)
            and (color == "any" or color in p_color)
            and min_price <= p_price <= max_price
        )

    # Filter the product catalog based on the match function
    recommendations = [p for p in product_catalog if match(p)]
    # Store the filtered recommendations back into context for downstream use
    context["recommendations"] = recommendations

    # If no products were found, prompt the user to refine preferences or retry image upload
    if not recommendations:
        print("\n❌ No matching products found.")
        # Debug information showing the criteria that failed to match anything
        print(f"🔍 DEBUG:\nbrand={brand}, category={category}, color={color}, price_range={min_price}-{max_price}")
        print("Would you like to:")
        print("1. Try again with different preferences")
        print("2. Upload another image")
        choice = input("Enter your choice (1/2): ").strip()
        if choice == "1":
            # Reset the product_type so that the clarifier will re-ask relevant questions
            context["reset_product_type"] = True
            return clarify_preferences(context)
        elif choice == "2":
            # Remove any existing image data and re-run image analysis
            context.pop("image_base64", None)
            return analyze_image(context)

    # If recommendations exist, print them out for the user
    print(f"\n✅ {len(recommendations)} matching products found:")
    for p in recommendations:
        print(f"- {p['name']} | ₹{p['price']} | {p['brand']} | {p['color']}")

    # Return the updated context (with recommendations) for any further processing
    return context
