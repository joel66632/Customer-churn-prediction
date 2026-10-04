import pandas as pd
import joblib
from django.conf import settings
import os

# Load once (important for performance)
MODEL_PATH = os.path.join(settings.BASE_DIR, "mainapp", "ml_model", "churn_random_forest_model.pkl")
SCALER_PATH = os.path.join(settings.BASE_DIR, "mainapp", "ml_model", "churn_scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

gender_map = {"male": 0, "female": 1}
subscription_map = {
    "basic": 0,
    "standard": 1,
    "premium": 2
}

def predict_churn(customer_dict):
    df = pd.DataFrame([customer_dict])

    # Encode
    df["Gender"] = df["Gender"].str.lower()
    df["Subscription Type"] = df["Subscription Type"].str.lower()

    df["Gender"] = df["Gender"].map(gender_map)
    df["Subscription Type"] = df["Subscription Type"].map(subscription_map)

    # Scale
    scaled_input = scaler.transform(df)

    # Predict
    prediction = model.predict(scaled_input)[0]
    probability = model.predict_proba(scaled_input)[0][1]
    risk_percentage = round(probability * 100, 2)

    # Risk logic
    risk_level, actions = get_retention_actions(probability)

    return {
        "prediction": int(prediction),
        "probability": risk_percentage,
        "risk_level": risk_level,
        "actions": actions,
    }


def get_retention_actions(probability):
    """
    Expanded business actions
    """

    if probability >= 0.85:
        return "CRITICAL RISK", [
            "Assign dedicated retention manager immediately",
            "Offer maximum loyalty discount (20–30%)",
            "Schedule urgent customer success call within 24 hours",
            "Provide premium support upgrade",
            "Conduct root-cause churn analysis",
            "Send personalized apology email",
        ]

    elif probability >= 0.70:
        return "HIGH RISK", [
            "Offer targeted discount (10–20%)",
            "Send personalized retention email",
            "Provide limited-time upgrade offer",
            "Trigger proactive support outreach",
            "Recommend relevant product features",
            "Add to high-priority monitoring list",
        ]

    elif probability >= 0.40:
        return "MEDIUM RISK", [
            "Send engagement email campaign",
            "Offer small loyalty reward",
            "Recommend product usage tips",
            "Monitor customer activity weekly",
            "Invite to feedback survey",
            "Promote feature adoption",
        ]

    else:
        return "LOW RISK", [
            "Maintain regular engagement",
            "Send appreciation message",
            "Upsell premium features",
            "Include in loyalty program",
            "Monitor monthly",
            "Encourage referrals",
        ]