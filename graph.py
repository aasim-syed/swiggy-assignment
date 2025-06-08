from langgraph.graph import StateGraph

from agents.image_analyzer import analyze_image
from agents.user_clarifier import clarify_preferences
from agents.product_recommender import recommend_products
from agents.enrich_preferences import enrich_preferences
from agents.capture_feedback import capture_feedback
from agents.similar_product import find_similar_products
from agents.summarize_session import summarize_session
from agents.confirm_product_type import confirm_product_type

# NEW AGENTS TO IMPORT
from agents.inventory_check import inventory_check
from agents.final_check import final_check
from agents.cart_manager import cart_manager


def build_graph():
    graph = StateGraph(dict)

    # === Existing nodes ===
    graph.add_node("ImageAnalysis", analyze_image)
    graph.add_node("ConfirmProductType", confirm_product_type)
    graph.add_node("Clarification", clarify_preferences)
    graph.add_node("PreferenceEnrichment", enrich_preferences)
    graph.add_node("ProductRecommendation", recommend_products)
    graph.add_node("CaptureFeedback", capture_feedback)
    graph.add_node("FindSimilarProducts", find_similar_products)
    graph.add_node("SummarizeSession", summarize_session)

    # === New feature nodes ===
    graph.add_node("InventoryCheck", inventory_check)
    graph.add_node("Confirmation", final_check)
    graph.add_node("CartManager", cart_manager)

    # === Define execution flow ===
    graph.set_entry_point("ImageAnalysis")
    graph.add_edge("ImageAnalysis", "ConfirmProductType")
    graph.add_edge("ConfirmProductType", "Clarification")
    graph.add_edge("Clarification", "PreferenceEnrichment")
    graph.add_edge("PreferenceEnrichment", "ProductRecommendation")
    
    # Insert inventory check after recommendation
    graph.add_edge("ProductRecommendation", "InventoryCheck")
    graph.add_edge("InventoryCheck", "Confirmation")
    graph.add_edge("Confirmation", "CartManager")

    # Conditional loop: If user wants to add more items, loop back
    # Define the router function for CartManager
    def cart_router(context):
        if context.get("add_more", False):
            return "Clarification"
        return "CaptureFeedback"

    # Replace old conditional edges with this
    graph.add_conditional_edges("CartManager", cart_router)

    # Remaining linear flow
    graph.add_edge("CaptureFeedback", "FindSimilarProducts")
    graph.add_edge("FindSimilarProducts", "SummarizeSession")

    return graph.compile()
