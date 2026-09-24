"""Collection operations for Experiment objects."""

from models import Experiment, ExperimentResult, Recipe, User


def create_experiment(
    experiments: list[Experiment],
    user: User,
    recipe: Recipe,
    change: str,
    temperature: int,
    duration_minutes: int,
    taste_score: int,
    experiment_date: str,
) -> Experiment:
    """Create an Experiment object and add it to the collection."""
    experiment_id = max((item.id for item in experiments), default=0) + 1
    result = ExperimentResult.from_score(taste_score)
    experiment = Experiment(
        experiment_id,
        user,
        recipe,
        change,
        temperature,
        duration_minutes,
        experiment_date,
        result,
    )
    experiments.append(experiment)
    return experiment


def cancel_experiment(
    experiments: list[Experiment],
    experiment_id: int,
) -> bool:
    """Find experiment and change its state through the object method."""
    for experiment in experiments:
        if experiment.id == experiment_id:
            experiment.cancel()
            return True
    return False


def get_recipe_experiments(
    experiments: list[Experiment],
    recipe: Recipe,
) -> list[Experiment]:
    """Return experiments related to a recipe object."""
    return [
        experiment
        for experiment in experiments
        if experiment.recipe is recipe
    ]


def calculate_statistics(experiments: list[Experiment]) -> dict[str, float]:
    """Calculate count and average score for active experiments."""
    active = [item for item in experiments if not item.is_cancelled]
    if not active:
        return {"count": 0, "average_score": 0.0}
    total = sum(item.result.taste_score for item in active)
    return {
        "count": len(active),
        "average_score": round(total / len(active), 2),
    }
