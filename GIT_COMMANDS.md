# Git для сквозного проекта

Репозиторий: https://github.com/welcometoforeverr/test-constructor

```powershell
git status
git log --oneline -10
git pull --ff-only
```

ПР9 выполнена в рабочей ветке `pr9-django-orm` от контрольной точки `0ec1325`.
Исходное состояние было чистым и уже сохранённым в Git. Коммиты доработки
начинаются с `PR9:`. После проверок изменения переносятся в main обычным
fast-forward и отправляются без принудительной перезаписи истории.

```powershell
git log --oneline --grep="^PR9:"
git status --short
```
