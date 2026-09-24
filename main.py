"""Console interface for the OOP version of the project."""

from datetime import date

from experiments import (
    calculate_statistics,
    cancel_experiment,
    create_experiment,
)
from models import Experiment, Recipe, User
from recipes import (
    add_recipe,
    filter_recipes_by_category,
    find_recipes,
    sort_recipes,
)
from storage import (
    load_experiments,
    load_recipes,
    load_users,
    save_experiments,
    save_recipes,
    save_users,
)
from utils import input_int

USERS_FILE = "data/users.json"
RECIPES_FILE = "data/recipes.json"
EXPERIMENTS_FILE = "data/experiments.json"


def show_recipes(recipes: list[Recipe]) -> None:
    """Print recipe objects."""
    if not recipes:
        print("Рецептов пока нет.")
        return
    for recipe in sort_recipes(recipes):
        print(f"{recipe.id}. {recipe}")


def show_experiments(experiments: list[Experiment]) -> None:
    """Print experiment objects."""
    if not experiments:
        print("Экспериментов пока нет.")
        return
    for experiment in experiments:
        print(f"{experiment.id}. {experiment}")


def find_recipe_by_id(
    recipes: list[Recipe],
    recipe_id: int,
) -> Recipe | None:
    """Return Recipe by id."""
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe
    return None


def ensure_default_user(users: list[User]) -> User:
    """Return first user or create a default project user."""
    if users:
        return users[0]
    user = User(1, "Калугин Никита", "nikita@example.com")
    users.append(user)
    return user


def main() -> None:
    """Run the application menu using collections of domain objects."""
    try:
        users = load_users(USERS_FILE)
        recipes = load_recipes(RECIPES_FILE)
        experiments = load_experiments(
            EXPERIMENTS_FILE,
            users,
            recipes,
        )
    except (ValueError, KeyError) as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    current_user = ensure_default_user(users)
    save_users(USERS_FILE, users)

    while True:
        print("\n=== Система учета кулинарных экспериментов ===")
        print(f"Пользователь: {current_user}")
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
            save_recipes(RECIPES_FILE, recipes)
            save_experiments(EXPERIMENTS_FILE, experiments)
            print("Данные сохранены. До свидания!")
            break

        try:
            if choice == "1":
                show_recipes(recipes)
            elif choice == "2":
                query = input("Введите часть названия: ")
                show_recipes(find_recipes(recipes, query))
            elif choice == "3":
                recipe = add_recipe(
                    recipes,
                    input("Название рецепта: "),
                    input("Категория: "),
                )
                save_recipes(RECIPES_FILE, recipes)
                print(f"Добавлен рецепт: {recipe}")
            elif choice == "4":
                show_recipes(recipes)
                recipe_id = input_int("ID рецепта: ", 1)
                recipe = find_recipe_by_id(recipes, recipe_id)
                if recipe is None:
                    print("Рецепт с таким ID не найден.")
                    continue
                experiment = create_experiment(
                    experiments,
                    current_user,
                    recipe,
                    input("Что изменили в рецепте: "),
                    input_int("Температура, °C: ", 1),
                    input_int("Время приготовления, мин: ", 1),
                    input_int("Оценка вкуса от 1 до 10: ", 1),
                    date.today().isoformat(),
                )
                save_experiments(EXPERIMENTS_FILE, experiments)
                print(f"Создан эксперимент: {experiment}")
            elif choice == "5":
                experiment_id = input_int("ID эксперимента: ", 1)
                if cancel_experiment(experiments, experiment_id):
                    save_experiments(EXPERIMENTS_FILE, experiments)
                    print("Эксперимент отменен.")
                else:
                    print("Эксперимент не найден.")
            elif choice == "6":
                show_experiments(experiments)
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
