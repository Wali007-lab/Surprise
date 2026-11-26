import pandas as pd

from surprise import Dataset, Reader, SVD

RATINGS = [
    ("1", "1", 5),
    ("1", "2", 4),
    ("2", "1", 3),
    ("2", "2", 5),
]


def compute_prediction(uid="1", iid="3"):
    """Train SVD on the sample ratings and return a prediction for (uid, iid)."""
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(
        pd.DataFrame(RATINGS, columns=["uid", "iid", "rating"]),
        reader,
    )
    trainset = data.build_full_trainset()

    algo = SVD(random_state=42)
    algo.fit(trainset)
    return algo.predict(uid, iid)


def format_prediction(prediction):
    """Format a Surprise Prediction object to one decimal place for display."""
    return f"Prediction: {prediction.est:.1f}"


def main():
    """Compute and display the formatted rating prediction."""
    prediction = compute_prediction()
    print(format_prediction(prediction))


if __name__ == "__main__":
    main()
