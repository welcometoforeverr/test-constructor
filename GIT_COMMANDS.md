# Команды Git для ПР1

После распаковки проекта можно использовать эти команды.

## Проверка локального репозитория

```bash
git status
git log --oneline
```

## Если создаёте собственный репозиторий заново

```bash
git init
git add .
git commit -m "Практическая работа 1: конструктор тестов"
```

## Подключение GitHub

Создайте пустой репозиторий, например `test-constructor`, затем выполните:

```bash
git branch -M main
git remote add origin https://github.com/USERNAME/test-constructor.git
git push -u origin main
```

Замените `USERNAME` на своё имя пользователя GitHub.

Если `origin` уже существует:

```bash
git remote -v
```

Ссылка на репозиторий понадобится в отчёте по ПР1.
