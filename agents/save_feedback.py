import os

def capture_feedback(context):
    mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"

    try:
        if mock_mode:
            print("[MOCK] Simulated feedback rating: 4")
            context["feedback_rating"] = 4
        else:
            print("\n📝 Please rate how helpful the recommendations were (1 = poor, 5 = excellent):")
            rating = int(input("Your rating: ").strip())
            context["feedback_rating"] = rating
    except:
        context["feedback_rating"] = None

    return context
