from experiments import (
    calculate_statistics,
    cancel_experiment,
    create_experiment,
    get_experiment_result,
    validate_experiment,
)


def test_validate_and_result() -> None:
    assert validate_experiment(180, 35, 9)
    assert get_experiment_result(True, 9) == "Эксперимент успешный"


def test_create_and_cancel_experiment() -> None:
    experiments = []
    created = create_experiment(
        experiments,
        1,
        "Меньше сахара",
        180,
        35,
        9,
        "2026-09-24",
    )
    assert created["id"] == 1
    assert cancel_experiment(experiments, 1)
    assert experiments == []


def test_statistics() -> None:
    experiments = [
        {"taste_score": 8},
        {"taste_score": 10},
    ]
    stats = calculate_statistics(experiments)
    assert stats == {"count": 2, "average_score": 9.0}
