import joblib
import pandas as pd
from src.preprocess import preprocess


def predict_next_6_hours():
    model = joblib.load("models/lounge_model.pkl")

    X, y = preprocess()

    last_row = X.iloc[-1].copy()
    predictions = []

    for i in range(6):
        # Move hour forward
        last_row["hour"] = (last_row["hour"] + 1) % 24

        pred = model.predict([last_row])[0]

        # Update previous hour crowd for next iteration
        last_row["prev_hour_crowd"] = pred

        predictions.append(round(pred, 2))

    return predictions


if __name__ == "__main__":
    preds = predict_next_6_hours()
    print("🔮 Next 6 Hour Predictions:")
    for i, p in enumerate(preds):
        print(f"Hour {i+1}: {p}")