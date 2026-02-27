import pandas as pd
import numpy as np

def generate_data(days=30):
    np.random.seed(42)
    
    hours = days * 24
    date_range = pd.date_range(
        end=pd.Timestamp.now(),
        periods=hours,
        freq='h'
    )
    
    data = pd.DataFrame()
    data["timestamp"] = date_range
    data["hour"] = data["timestamp"].dt.hour
    data["day_of_week"] = data["timestamp"].dt.dayofweek
    data["is_weekend"] = data["day_of_week"].isin([5, 6]).astype(int)
    
    # Simulate flight activity
    data["flights"] = np.random.poisson(lam=5, size=hours)
    data["avg_passengers"] = np.random.randint(80, 220, size=hours)
    
    base_crowd = 30
    
    data["crowd"] = (
        base_crowd
        + data["hour"].apply(lambda x: 60 if 17 <= x <= 21 else 40 if 6 <= x <= 9 else 10)
        + data["is_weekend"] * 20
        + data["flights"] * 5
        + (data["avg_passengers"] * 0.15)
    )
    
    # Add some randomness
    data["crowd"] += np.random.normal(0, 10, size=hours)
    
    return data


if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/raw/lounge_data.csv", index=False)
    print("✅ Synthetic lounge data generated successfully.")