# ПР9 — подготовка к защите

Данные проходят цепочку Django view → QuerySet → SQL, сформированный ORM →
SQLite → объекты моделей → контекст → Django template.
Консоль использует тот же ORM через db/repository.py; исходные классы ПР3 сохранены.

## Что показать

1. `web_recipes/models.py` и `web_experiments/models.py`: поля, ForeignKey,
   OneToOneField, PROTECT, CASCADE, related_name и ограничения.
2. `python manage.py showmigrations`: обе миграции приложений отмечены [X].
3. `import_legacy.py`: источник только для чтения, полный перенос в transaction.atomic,
   запрет перезаписи непустой базы, full_clean, сохранение ID и контроль количества.
4. `/recipes/?q=кекс&category=Выпечка` и карточку рецепта: поиск и агрегаты.
5. `/experiments/`: поиск сразу по 3 полям, фильтры, сортировка и пагинация.
6. Создать несколько опытов через консоль или shell. Размер страницы — 5 в
   `web_experiments/views.py`. Шаблон `includes/pagination.html` применяет
   `{% querystring %}`: меняется page, остальные параметры остаются.
7. `/experiments/statistics/`: Count, Avg, Min, Max, Sum, группировка через annotate.
   Рецепты без опытов сохраняются в статистике с нулевым Count.
8. Отменить опыт из консоли: запись остаётся, статус становится «Отменен»,
   фильтр «Действующие» исключает её через exclude().
9. Показать check, pytest, flake8, HTTP smoke и GitHub Actions.

## Django shell

```python
from web_recipes.models import Recipe
from web_experiments.models import User, Experiment, ExperimentResult
from web_experiments.queries import experiment_catalog, experiment_statistics
from db.repository import delete_saved_experiment

user = User.objects.get(pk=1)
recipe = Recipe.objects.create(name="Тестовый суп", category="Супы")
experiment = Experiment.objects.create(
    user=user, recipe=recipe, change_description="Новая специя",
    temperature=95, duration_minutes=25,
)
result = ExperimentResult(experiment=experiment, taste_score=8,
                          status="Эксперимент успешный")
result.full_clean()
result.save()
experiment.cancel()
list(user.experiments.all())
list(experiment_catalog({"status": "active", "sort": "score"}))
experiment_statistics()
delete_saved_experiment(experiment.pk)
recipe.delete()
```

create() сразу сохраняет объект. save() сохраняет новый объект или изменения
существующего. Методы save()/create() сами не вызывают full_clean(): в адаптере
консоли и команде переноса валидация вызывается явно. Ограничения БД работают
независимо от вызова валидации. Демонстрационные действия выполняйте на копии базы.

get() возвращает один объект и вызывает DoesNotExist либо MultipleObjectsReturned
при нуле или нескольких совпадениях. filter() возвращает QuerySet; first() —
объект или None. Карточки обрабатывают None собственным шаблоном с HTTP 404.

select_related("recipe", "user", "result") загружает связанные объекты одним
запросом вместо запроса для каждой карточки. Это проверено числом запросов в тесте.
annotate() добавляет показатель для каждой записи/группы, aggregate() возвращает
общий словарь показателей. values() определяет поля группировки.

makemigrations создаёт описание структуры, migrate применяет его к базе.
`sqlmigrate web_experiments 0001` показывает SQL миграции без её выполнения.
Старые таблицы не выдаются за миграции через --fake: выбран перенос в новую базу.

Сначала выполняются фильтры, затем order_by, затем Paginator. Вторичный ключ id
стабилизирует порядок при одинаковых датах/оценках. get_page() обрабатывает
нечисловые страницы как первую, страницы вне диапазона — как последнюю.
Поле сортировки выбирается только из SORTS, а дата, оценка и recipe проверяются формой.

Материалы Яндекс Практикума выполнены и показаны преподавателю по подтверждению студента.
