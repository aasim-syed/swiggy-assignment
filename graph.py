from langgraph.graph import StateGraph
from agents.image_analyzer import analyze_image
from agents.user_clarifier import clarify_preferences
from agents.product_recommender import recommend_product
from agents.enrich_prefreneces import enrich_preferences
from agents.save_feedback import capture_feedback
from agents.similar_products import find_similar_products
from agents.summarize import summarize_session
from agents.product_confirmation import confirm_product_type  # Optional but implemented

def build_graph():
    graph = StateGraph(dict)

    # === Add all nodes ===
    graph.add_node("ImageAnalysis", analyze_image)
    graph.add_node("ConfirmProductType", confirm_product_type)
    graph.add_node("Clarification", clarify_preferences)
    graph.add_node("PreferenceEnrichment", enrich_preferences)
    graph.add_node("ProductRecommendation", recommend_product)
    graph.add_node("CaptureFeedback", capture_feedback)
    graph.add_node("FindSimilarProducts", find_similar_products)
    graph.add_node("SummarizeSession", summarize_session)

    # === Define execution flow ===
    graph.set_entry_point("ImageAnalysis")
    graph.add_edge("ImageAnalysis", "ConfirmProductType")
    graph.add_edge("ConfirmProductType", "Clarification")
    graph.add_edge("Clarification", "PreferenceEnrichment")
    graph.add_edge("PreferenceEnrichment", "ProductRecommendation")
    graph.add_edge("ProductRecommendation", "CaptureFeedback")
    graph.add_edge("CaptureFeedback", "FindSimilarProducts")
    graph.add_edge("FindSimilarProducts", "SummarizeSession")

    return graph.compile()
