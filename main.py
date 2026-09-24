"""Console interface for the culinary experiments accounting system."""

from datetime import date

from experiments import (
    calculate_statistics,
    cancel_experiment,
    create_experiment,
)
from recipes import (
    add_recipe,
    filter_recipes_by_category,
    find_recipes,
    sort_recipes,
)
from storage import load_data, save_data
from utils import input_int

RECIPES_FILE = "data/recipes.json"
EXPERIMENTS_FILE = "data/experiments.json"


def show_recipes(recipes: list[dict]) -> None:
    """Print recipes sorted by name."""
    if not recipes:
        print("Рецептов пока нет.")
        return
    for recipe in sort_recipes(recipes):
        print(f'{recipe["id"]}. {recipe["name"]} ({recipe["category"]})')


def show_experiments(experiments: list[dict], recipes: list[dict]) -> None:
    """Print culinary experiments with their recipe names."""
    if not experiments:
        print("Экспериментов пока нет.")
        return
    recipe_names = {recipe["id"]: recipe["name"] for recipe in recipes}
    for experiment in experiments:
        recipe_name = recipe_names.get(
            experiment["recipe_id"],
            "Неизвестный рецепт",
        )
        print(
            f'{experiment["id"]}. {recipe_name}: '
            f'{experiment["change"]}; {experiment["result"]}; '
            f'оценка {experiment["taste_score"]}/10'
        )


def find_recipe_by_id(recipes: list[dict], recipe_id: int) -> dict | None:
    """Return a recipe by identifier or None."""
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return recipe
    return None


def main() -> None:
    """Run the application menu and save all changes to JSON files."""
    try:
        recipes = load_data(RECIPES_FILE)
        experiments = load_data(EXPERIMENTS_FILE)
    except ValueError as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    while True:
        print("\n=== Система учета кулинарных экспериментов ===")
        print("1. Показать рецепты")
        print("2. Найти рецепт")
        print("3. Добавить рецепт")
        print("4. Добавить эксперимент")
        print("5. Отменить эксперимент")
        print("6. Показать эксперименты")
        print("7. Показать статистику")
        print("8. Фильтр рецептов по категории")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            save_data(RECIPES_FILE, recipes)
            save_data(EXPERIMENTS_FILE, experiments)
            print("Данные сохранены. До свидания!")
            break

        try:
            if choice == "1":
                show_recipes(recipes)
            elif choice == "2":
                query = input("Введите часть названия: ")
                show_recipes(find_recipes(recipes, query))
            elif choice == "3":
                name = input("Название рецепта: ")
                category = input("Категория: ")
                recipe = add_recipe(recipes, name, category)
                save_data(RECIPES_FILE, recipes)
                print(f'Добавлен рецепт: {recipe["name"]}')
            elif choice == "4":
                show_recipes(recipes)
                recipe_id = input_int("ID рецепта: ", 1)
                if find_recipe_by_id(recipes, recipe_id) is None:
                    print("Рецепт с таким ID не найден.")
                    continue
                change = input("Что изменили в рецепте: ")
                temperature = input_int("Температура, °C: ", 1)
                duration = input_int("Время приготовления, мин: ", 1)
                score = input_int("Оценка вкуса от 1 до 10: ", 1)
                experiment = create_experiment(
                    experiments,
                    recipe_id,
                    change,
                    temperature,
                    duration,
                    score,
                    date.today().isoformat(),
                )
                save_data(EXPERIMENTS_FILE, experiments)
                print(f'Результат: {experiment["result"]}')
            elif choice == "5":
                experiment_id = input_int("ID эксперимента: ", 1)
                if cancel_experiment(experiments, experiment_id):
                    save_data(EXPERIMENTS_FILE, experiments)
                    print("Эксперимент удален.")
                else:
                    print("Эксперимент не найден.")
            elif choice == "6":
                show_experiments(experiments, recipes)
            elif choice == "7":
                stats = calculate_statistics(experiments)
                print(f'Количество экспериментов: {int(stats["count"])}')
                print(f'Средняя оценка: {stats["average_score"]}')
            elif choice == "8":
                category = input("Категория: ")
                filtered = list(filter_recipes_by_category(recipes, category))
                show_recipes(filtered)
            else:
                print("Неизвестный пункт меню.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
