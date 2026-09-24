from models import Experiment, ExperimentResult, Recipe, User
from storage import (
    load_experiments,
    load_recipes,
    load_users,
    save_experiments,
    save_recipes,
    save_users,
)


def test_object_json_round_trip(tmp_path) -> None:
    users_file = tmp_path / "users.json"
    recipes_file = tmp_path / "recipes.json"
    experiments_file = tmp_path / "experiments.json"

    user = User(1, "Никита", "n@example.com")
    recipe = Recipe(1, "Кекс", "Выпечка")
    experiment = Experiment(
        1,
        user,
        recipe,
        "Меньше сахара",
        180,
        35,
        "2026-09-24",
        ExperimentResult.from_score(9),
    )

    save_users(str(users_file), [user])
    save_recipes(str(recipes_file), [recipe])
    save_experiments(str(experiments_file), [experiment])

    users = load_users(str(users_file))
    recipes = load_recipes(str(recipes_file))
    experiments = load_experiments(
        str(experiments_file),
        users,
        recipes,
    )

    assert isinstance(users[0], User)
    assert isinstance(recipes[0], Recipe)
    assert isinstance(experiments[0], Experiment)
    assert experiments[0].user is users[0]
    assert experiments[0].recipe is recipes[0]
