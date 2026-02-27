import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from preprocess import preprocess


def train():
    X, y = preprocess()

    # Time-series split (no shuffle)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    print(f"✅ Model trained successfully.")
    print(f"Model MAE: {mae:.2f}")

    joblib.dump(model, "models/lounge_model.pkl")
    print("✅ Model saved inside /models folder.")


if __name__ == "__main__":
    train()