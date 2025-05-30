from langgraph.graph import StateGraph
from agents.image_analyzer import analyze_image
from agents.user_clarifier import clarify_preferences
from agents.product_recommender import recommend_product

def build_graph():
    graph = StateGraph(dict)
    graph.add_node("ImageAnalysis", analyze_image)
    graph.add_node("Clarification", clarify_preferences)
    graph.add_node("ProductRecommendation", recommend_product)

    graph.set_entry_point("ImageAnalysis")
    graph.add_edge("ImageAnalysis", "Clarification")
    graph.add_edge("Clarification", "ProductRecommendation")

    return graph.compile()
