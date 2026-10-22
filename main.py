"""Console UI for the shared SQLite-backed culinary experiments system."""
import sqlite3
from datetime import date

from db.repository import (
    cancel_saved_experiment,
    load_catalog,
    save_experiment,
    save_recipe,
    save_user,
)
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
from utils import input_int


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
    """Manage recipes and experiments in SQLite through the console."""
    try:
        users, recipes, experiments = load_catalog()
        current_user = ensure_default_user(users)
        save_user(current_user)
    except (ValueError, KeyError, sqlite3.Error) as error:
        print(f"Ошибка загрузки данных: {error}")
        return

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
            print("Изменения уже сохранены в общей базе SQLite.")
            break

        try:
            if choice == "1":
                show_recipes(recipes)
            elif choice == "2":
                show_recipes(find_recipes(recipes, input("Часть названия: ")))
            elif choice == "3":
                recipe = add_recipe(
                    recipes,
                    input("Название рецепта: "),
                    input("Категория: "),
                )
                save_recipe(recipe)
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
                save_experiment(experiment)
                print(f"Создан эксперимент: {experiment}")
            elif choice == "5":
                experiment_id = input_int("ID эксперимента: ", 1)
                if cancel_saved_experiment(experiment_id):
                    cancel_experiment(experiments, experiment_id)
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
                show_recipes(list(filter_recipes_by_category(recipes, category)))
            else:
                print("Неизвестный пункт меню.")
        except (ValueError, sqlite3.Error) as error:
            print(f"Ошибка: {error}")
            users, recipes, experiments = load_catalog()


if __name__ == "__main__":
    main()
