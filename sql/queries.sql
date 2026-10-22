-- CulinaryLab: SQL-запросы ПР7
-- Значения вместо ? передаются параметризованно из Python.

-- 1. SELECT: список рецептов
SELECT id, name, category
FROM recipes
ORDER BY name;

-- 2. SELECT: список пользователей
SELECT id, name, email
FROM users
ORDER BY name;

-- 3. WHERE: поиск рецептов по категории
SELECT id, name, category
FROM recipes
WHERE category = ?
ORDER BY name;

-- 4. WHERE: эксперименты с оценкой не ниже заданной
SELECT e.id, e.recipe_id, r.taste_score, r.status
FROM experiments AS e
JOIN experiment_results AS r ON r.experiment_id = e.id
WHERE r.taste_score >= ?
ORDER BY r.taste_score DESC, e.id;

-- 5. JOIN: полный список экспериментов
SELECT
    e.id,
    e.experiment_date,
    e.change_description,
    e.temperature,
    e.duration_minutes,
    e.is_cancelled,
    recipes.id AS recipe_id,
    recipes.name AS recipe_name,
    users.name AS user_name,
    r.taste_score,
    r.status
FROM experiments AS e
JOIN recipes ON recipes.id = e.recipe_id
JOIN users ON users.id = e.user_id
JOIN experiment_results AS r ON r.experiment_id = e.id
ORDER BY e.experiment_date DESC, e.id DESC;

-- 6. JOIN: история экспериментов конкретного рецепта
SELECT
    recipes.id AS recipe_id,
    recipes.name AS recipe_name,
    e.id AS experiment_id,
    e.experiment_date,
    r.taste_score,
    r.status
FROM recipes
LEFT JOIN experiments AS e ON e.recipe_id = recipes.id
LEFT JOIN experiment_results AS r ON r.experiment_id = e.id
WHERE recipes.id = ?
ORDER BY e.experiment_date DESC;

-- 7. AGGREGATE: общее количество экспериментов
SELECT COUNT(*) AS experiments_count
FROM experiments;

-- 8. AGGREGATE: средняя, минимальная и максимальная оценка
SELECT
    ROUND(AVG(taste_score), 2) AS average_score,
    MIN(taste_score) AS min_score,
    MAX(taste_score) AS max_score
FROM experiment_results;

-- 9. GROUP BY: количество экспериментов по рецептам
SELECT
    recipes.id,
    recipes.name,
    COUNT(e.id) AS experiments_count
FROM recipes
LEFT JOIN experiments AS e ON e.recipe_id = recipes.id
GROUP BY recipes.id, recipes.name
ORDER BY experiments_count DESC, recipes.name;

-- 10. GROUP BY: количество рецептов по категориям
SELECT category, COUNT(*) AS recipes_count
FROM recipes
GROUP BY category
ORDER BY recipes_count DESC, category;

-- 11. GROUP BY: результаты по статусам
SELECT
    status,
    COUNT(*) AS results_count,
    ROUND(AVG(taste_score), 2) AS average_score
FROM experiment_results
GROUP BY status
ORDER BY results_count DESC, status;

-- 12. GROUP BY + HAVING: рецепты со средней оценкой от заданной
SELECT
    recipes.id,
    recipes.name,
    ROUND(AVG(r.taste_score), 2) AS average_score,
    COUNT(r.id) AS experiments_count
FROM recipes
JOIN experiments AS e ON e.recipe_id = recipes.id
JOIN experiment_results AS r ON r.experiment_id = e.id
GROUP BY recipes.id, recipes.name
HAVING AVG(r.taste_score) >= ?
ORDER BY average_score DESC, recipes.name;

-- 13. WHERE: активные эксперименты
SELECT id, recipe_id, experiment_date
FROM experiments
WHERE is_cancelled = 0
ORDER BY experiment_date DESC;

-- 14. JOIN + WHERE: успешные активные эксперименты
SELECT
    e.id,
    recipes.name AS recipe_name,
    r.taste_score,
    r.status
FROM experiments AS e
JOIN recipes ON recipes.id = e.recipe_id
JOIN experiment_results AS r ON r.experiment_id = e.id
WHERE e.is_cancelled = 0
  AND r.taste_score >= 8
ORDER BY r.taste_score DESC;
