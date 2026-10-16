"""Запуск базовых проверок без pytest: python run_tests.py"""
from app import create_app


def main():
    app = create_app()
    client = app.test_client()
    catalog_sorted = client.get("/catalog?sort=price_asc")
    checks = [
        ("GET /", client.get("/").status_code, 200),
        ("GET /catalog", client.get("/catalog").status_code, 200),
        ("GET /catalog?sort=price_asc", catalog_sorted.status_code, 200),
        ("GET /auth/login", client.get("/auth/login").status_code, 200),
        ("GET /booking/1 (без входа)", client.get("/booking/1").status_code, 302),
    ]
    if catalog_sorted.status_code == 200 and "Найдено мероприятий" not in catalog_sorted.get_data(as_text=True):
        print("FAIL: GET /catalog?sort=price_asc -> нет счётчика результатов")
        return 1
    failed = 0
    for name, got, expected in checks:
        ok = got == expected
        print(f"{'OK' if ok else 'FAIL'}: {name} -> {got} (ожид. {expected})")
        if not ok:
            failed += 1
    print("-" * 40)
    print("Пройдено:" if failed == 0 else "Ошибок:", len(checks) - failed, "из", len(checks))
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
