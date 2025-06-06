def summarize_session(context):
    preferences = context.get("preferences", {})
    recommendations = context.get("recommendations", [])
    feedback = context.get("feedback_rating", None)

    summary = "\n🧾 Session Summary:\n"
    summary += f"Your preferences were: {preferences}\n"
    if feedback:
        summary += f"Your feedback rating: {feedback}/5\n"

    if recommendations:
        summary += "Recommended products:\n"
        for rec in recommendations:
            summary += f"- {rec.get('name', 'Unknown')} (₹{rec.get('price', 'N/A')})\n"
    else:
        summary += "No matching or similar products found.\n"

    context["session_summary"] = summary
    print(summary)
    return context
