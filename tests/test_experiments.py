from experiments import (
    calculate_statistics,
    cancel_experiment,
    create_experiment,
)
from models import Recipe, User


def test_create_cancel_and_statistics() -> None:
    user = User(1, "Никита", "n@example.com")
    recipe = Recipe(1, "Кекс", "Выпечка")
    experiments = []
    experiment = create_experiment(
        experiments,
        user,
        recipe,
        "Меньше сахара",
        180,
        35,
        9,
        "2026-09-24",
    )
    assert experiment.result.status == "Эксперимент успешный"
    assert calculate_statistics(experiments)["average_score"] == 9.0
    assert cancel_experiment(experiments, experiment.id)
    assert calculate_statistics(experiments)["count"] == 0
