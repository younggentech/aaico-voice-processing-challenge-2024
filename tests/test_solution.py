"""Use this file to evaluate the model's performance"""

import numpy as np
import pytest
from src.solution.main import get_predictions


@pytest.fixture(name="results")
def load_results():
    """Get the np.array with prediction data."""
    return get_predictions()


def test_validity(results):
    """Code is taken from the colab file."""
    overrun_times_ms = (results[2] - results[0]) / 1e6
    assert np.all(
        np.diff(results[2]) >= 0
    )  # Labelling has been done sequentially
    assert np.all(
        overrun_times_ms <= 50
    )  # Processing took less than 50 ms for each sample


def test_score(results): ...
