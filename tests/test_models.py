from models import Experiment, ExperimentResult, Recipe, User


def test_recipe_str_and_validation() -> None:
    recipe = Recipe(1, "Кекс", "Выпечка")
    assert str(recipe) == "Кекс (Выпечка)"
    assert Recipe.validate_name("Суп")


def test_result_from_score() -> None:
    result = ExperimentResult.from_score(9)
    assert result.status == "Эксперимент успешный"
    assert result.taste_score == 9


def test_experiment_composition_and_cancel() -> None:
    user = User(1, "Никита", "n@example.com")
    recipe = Recipe(1, "Кекс", "Выпечка")
    result = ExperimentResult.from_score(8)
    experiment = Experiment(
        1,
        user,
        recipe,
        "Меньше сахара",
        180,
        30,
        "2026-09-24",
        result,
    )
    assert experiment.recipe is recipe
    assert experiment.user is user
    experiment.cancel()
    assert experiment.is_cancelled
    assert experiment.status == "Отменен"
