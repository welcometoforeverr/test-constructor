"""Functions for working with culinary experiments."""


def validate_experiment(
    temperature: int,
    duration_minutes: int,
    taste_score: int,
) -> bool:
    """Check whether the main experiment parameters are valid."""
    return (
        temperature > 0
        and duration_minutes > 0
        and 1 <= taste_score <= 10
    )


def get_experiment_result(is_valid: bool, taste_score: int) -> str:
    """Return a text result for a culinary experiment."""
    if not is_valid:
        return "Эксперимент заполнен некорректно"
    if taste_score >= 8:
        return "Эксперимент успешный"
    if taste_score >= 5:
        return "Результат удовлетворительный"
    return "Эксперимент неудачный"


def create_experiment(
    experiments: list[dict],
    recipe_id: int,
    change_description: str,
    temperature: int,
    duration_minutes: int,
    taste_score: int,
    experiment_date: str,
) -> dict:
    """Validate parameters and add a culinary experiment."""
    if not validate_experiment(temperature, duration_minutes, taste_score):
        raise ValueError("Некорректные параметры эксперимента")
    if not change_description.strip():
        raise ValueError("Описание изменения не может быть пустым")

    result = get_experiment_result(True, taste_score)
    experiment = {
        "id": max((item["id"] for item in experiments), default=0) + 1,
        "recipe_id": recipe_id,
        "change": change_description.strip(),
        "temperature": temperature,
        "duration_minutes": duration_minutes,
        "taste_score": taste_score,
        "date": experiment_date,
        "result": result,
    }
    experiments.append(experiment)
    return experiment


def cancel_experiment(experiments: list[dict], experiment_id: int) -> bool:
    """Delete an experiment by identifier and report whether it was found."""
    for index, experiment in enumerate(experiments):
        if experiment["id"] == experiment_id:
            del experiments[index]
            return True
    return False


def get_recipe_experiments(
    experiments: list[dict],
    recipe_id: int,
) -> list[dict]:
    """Return all experiments associated with a recipe."""
    return [
        experiment
        for experiment in experiments
        if experiment["recipe_id"] == recipe_id
    ]


def calculate_statistics(experiments: list[dict]) -> dict[str, float]:
    """Calculate experiment count and average taste score."""
    if not experiments:
        return {"count": 0, "average_score": 0.0}

    total_score = 0
    for experiment in experiments:
        total_score += experiment["taste_score"]

    return {
        "count": len(experiments),
        "average_score": round(total_score / len(experiments), 2),
    }
