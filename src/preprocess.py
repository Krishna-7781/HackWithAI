import pandas as pd

def preprocess():
    df = pd.read_csv("data/raw/lounge_data.csv")

    # Add previous hour crowd feature
    df["prev_hour_crowd"] = df["crowd"].shift(1)

    # Remove first row (because shift creates NaN)
    df = df.dropna()

    # Features for model
    features = [
        "hour",
        "day_of_week",
        "is_weekend",
        "flights",
        "avg_passengers",
        "prev_hour_crowd"
    ]

    X = df[features]
    y = df["crowd"]

    # Save processed file
    df.to_csv("data/processed/processed_data.csv", index=False)

    print("✅ Preprocessing complete.")
    return X, y


if __name__ == "__main__":
    preprocess()