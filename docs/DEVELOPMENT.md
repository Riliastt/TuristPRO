# Процесс разработки TuristPRO

Документ описывает, как Git встроен в жизненный цикл разработки.

## Модель ветвления

Используется **GitHub Flow**:

```text
master  ←── Pull Request ←── feature/* | fix/* | docs/* | ci/*
```

- `master` — стабильная ветка, всегда готова к запуску.
- Задачи выполняются в коротких feature-ветках.
- Слияние только через Pull Request после CI.

## Этапы изменения

1. **Планирование** — Issue (баг / улучшение).
2. **Разработка** — ветка от `master`, локальные коммиты.
3. **Проверка** — `python run_tests.py`, затем Push.
4. **Интеграция** — Pull Request, code review, GitHub Actions.
5. **Релиз** — merge в `master`, при необходимости Git tag / Release.

## Continuous Integration

Workflow: `.github/workflows/ci.yml`

| Job | Назначение |
|-----|------------|
| Smoke tests | Проверка ключевых HTTP-маршрутов |
| Lint | Статический анализ Python (Ruff) |

## Версионирование

- Теги формата `vMAJOR.MINOR.PATCH` (SemVer).
- Описание релиза — в GitHub Releases и `CHANGELOG.md`.
