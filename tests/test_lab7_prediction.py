"""Automated verification tests for Lab 7 Task 3 prediction formatting."""

from pathlib import Path
import re
import subprocess
import sys

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from lab7.predict_rating import compute_prediction, format_prediction, RATINGS
from surprise import Dataset, Prediction, Reader, SVD


def test_format_prediction_uses_one_decimal_place():
    """Formatted output uses one decimal place and differs from unrounded."""
    sample = Prediction("1", "3", None, 2.3456, {"was_impossible": False})
    formatted = format_prediction(sample)

    assert formatted == "Prediction: 2.3"
    assert formatted != f"Prediction: {sample.est}"
    assert re.fullmatch(r"Prediction: -?\d+\.\d", formatted)


def test_predict_rating_behavior_and_unchanged_estimate():
    """Verify 1-decimal display while preserving the underlying SVD estimate."""
    prediction = compute_prediction("1", "3")
    formatted = format_prediction(prediction)

    assert prediction.details["was_impossible"] is False
    assert 1.0 <= prediction.est <= 5.0
    assert formatted == f"Prediction: {prediction.est:.1f}"
    assert re.fullmatch(r"Prediction: -?\d+\.\d", formatted)

    # Verify underlying calculation matches the original SVD(random_state=42) setup.
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(
        pd.DataFrame(RATINGS, columns=["uid", "iid", "rating"]),
        reader,
    )
    baseline_algo = SVD(random_state=42)
    baseline_algo.fit(data.build_full_trainset())
    baseline_prediction = baseline_algo.predict("1", "3")

    assert prediction.est == baseline_prediction.est


def test_predict_rating_cli_output():
    """CLI script output matches format_prediction(compute_prediction())."""
    script_path = ROOT_DIR / "lab7" / "predict_rating.py"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    expected = format_prediction(compute_prediction("1", "3"))

    assert output == expected
    assert re.fullmatch(r"Prediction: -?\d+\.\d", output)
