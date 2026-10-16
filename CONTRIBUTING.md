# Регламент работы с Git (GitHub Flow)

В проекте TuristPRO используется модель **GitHub Flow**: короткие ветки под задачу и слияние через Pull Request.

## Основные правила

1. Ветка `master` всегда в рабочем состоянии.
2. Новая задача — новая ветка от актуального `master`.
3. Изменения попадают в `master` только через Pull Request.
4. Перед слиянием нужно пройти code review и проверки CI (GitHub Actions).

## Именование веток

| Тип | Пример |
|-----|--------|
| Новая функция | `feature/add-catalog-filter` |
| Исправление | `fix/login-redirect` |
| Документация | `docs/update-readme` |

## Сообщения коммитов

Кратко и по делу, на английском или русском, в повелительном наклонении:

- `Add contributing guide with GitHub Flow`
- `Fix booking status display`
- `Update README run instructions`

## Порядок работы

```text
1. git checkout master
2. git pull
3. git checkout -b feature/my-change
4. Внесите правки и закоммитьте
5. git push -u origin feature/my-change
6. Откройте Pull Request в GitHub
7. После review — Merge
8. Удалите ветку (по желанию)
```

## Code review

В Pull Request проверяют:

- корректность изменений;
- понятность коммитов и описания PR;
- отсутствие секретов (пароли, ключи, `.env`);
- прохождение автопроверок CI (workflow `.github/workflows/ci.yml`).

## Issues и шаблоны

- Ошибки оформляются через шаблон **Ошибка**.
- Предложения — через шаблон **Улучшение**.
- Pull Request заполняется по `.github/PULL_REQUEST_TEMPLATE.md`.

## Continuous Integration

При каждом Push и Pull Request в `master` GitHub Actions:

1. устанавливает Python и зависимости из `requirements.txt`;
2. запускает `python run_tests.py` (smoke-тесты маршрутов).

Зелёный статус проверки — обязательное условие для merge.
