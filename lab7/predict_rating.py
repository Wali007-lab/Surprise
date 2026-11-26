from surprise import Dataset
from surprise import Reader
from surprise import SVD

ratings = [
    ("1", "1", 5),
    ("1", "2", 4),
    ("2", "1", 3),
    ("2", "2", 5),
]

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(
    __import__("pandas").DataFrame(ratings, columns=["uid", "iid", "rating"]),
    reader,
)

trainset = data.build_full_trainset()

algo = SVD(random_state=42)
algo.fit(trainset)

prediction = algo.predict("1", "3")

print(f"Prediction: {prediction.est}")