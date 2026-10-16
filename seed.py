"""Заполнение базы тестовыми данными для демонстрации диплома."""
from datetime import datetime, timedelta, timezone

from app import create_app, db
from app.models import (
    Activity,
    Booking,
    BookingStatus,
    Category,
    Payment,
    PaymentStatus,
    Role,
    Schedule,
    User,
)

# Локальные изображения, чтобы карточки работали без интернета и внешних CDN.
IMG = {
    "old_town": "/static/img/activities/excursion.svg",
    "cheese": "/static/img/activities/gastronomy.svg",
    "pottery": "/static/img/activities/masterclass.svg",
    "castle": "/static/img/activities/history.svg",
    "photo": "/static/img/activities/masterclass.svg",
    "market": "/static/img/activities/gastronomy.svg",
    "river": "/static/img/activities/excursion.svg",
    "museum": "/static/img/activities/history.svg",
    "wine": "/static/img/activities/gastronomy.svg",
    "bike": "/static/img/activities/excursion.svg",
    "cooking": "/static/img/activities/gastronomy.svg",
    "theater": "/static/img/activities/history.svg",
}

CATEGORIES = [
    ("Экскурсия", "excursion"),
    ("Мастер-класс", "masterclass"),
    ("Гастрономия", "gastronomy"),
    ("История", "history"),
]

ACCOUNTS = [
    # Администраторы
    ("admin@turistpro.ru", "Администратор Системы", "+79001000001", Role.ADMIN, "admin123"),
    # Организаторы
    ("organizer@turistpro.ru", "Иван Петров", "+79002000001", Role.ORGANIZER, "organizer123"),
    ("elena.tours@turistpro.ru", "Елена Смирнова", "+79002000002", Role.ORGANIZER, "organizer123"),
    ("art.studio@turistpro.ru", "Алексей Кузнецов", "+79002000003", Role.ORGANIZER, "organizer123"),
    # Туристы
    ("tourist@turistpro.ru", "Мария Иванова", "+79003000001", Role.TOURIST, "tourist123"),
    ("dmitry@turistpro.ru", "Дмитрий Волков", "+79003000002", Role.TOURIST, "tourist123"),
    ("anna@turistpro.ru", "Анна Соколова", "+79003000003", Role.TOURIST, "tourist123"),
    ("guest.demo@turistpro.ru", "Олег Новиков", "+79003000004", Role.TOURIST, "tourist123"),
]

# organizer_email -> список мероприятий
ACTIVITIES = [
    {
        "organizer": "organizer@turistpro.ru",
        "title": "Прогулка по старому городу",
        "description": (
            "Пешеходная экскурсия по историческому центру с профессиональным гидом. "
            "Узнайте легенды улиц, дворов-колодцев и архитектурные тайны города."
        ),
        "location": "Площадь Собора, 1",
        "price": 1200,
        "duration": 90,
        "category": "excursion",
        "image": IMG["old_town"],
    },
    {
        "organizer": "organizer@turistpro.ru",
        "title": "Тайны средневекового замка",
        "description": (
            "Экскурсия по замковому комплексу: башни, подземелья и смотровые площадки. "
            "Идеально для любителей истории."
        ),
        "location": "Замковая гора",
        "price": 1500,
        "duration": 100,
        "category": "history",
        "image": IMG["castle"],
    },
    {
        "organizer": "organizer@turistpro.ru",
        "title": "Велопрогулка вдоль набережной",
        "description": (
            "Активная экскурсия на велосипедах с остановками у главных видовых точек. "
            "Включены велосипед и шлем."
        ),
        "location": "Набережная, 3 (пункт проката)",
        "price": 1600,
        "duration": 120,
        "category": "excursion",
        "image": IMG["bike"],
    },
    {
        "organizer": "elena.tours@turistpro.ru",
        "title": "Дегустация местных сыров",
        "description": (
            "Гастрономический тур по сыроварне: дегустация 6 сортов, "
            "мастер-класс по нарезке и рассказ о технологии созревания."
        ),
        "location": "ул. Ремесленная, 15",
        "price": 1800,
        "duration": 60,
        "category": "gastronomy",
        "image": IMG["cheese"],
    },
    {
        "organizer": "elena.tours@turistpro.ru",
        "title": "Гастро-рынок: вкусы региона",
        "description": (
            "Экскурсия по центральному рынку с дегустацией фермерских продуктов, "
            "мёда, варенья и местной выпечки."
        ),
        "location": "Центральный рынок, павильон 2",
        "price": 900,
        "duration": 75,
        "category": "gastronomy",
        "image": IMG["market"],
    },
    {
        "organizer": "elena.tours@turistpro.ru",
        "title": "Винная дегустация в погребе",
        "description": (
            "Знакомство с местными виноделами: 5 вин, сыры и закуски. "
            "Рассказ о терруаре и сортах винограда региона."
        ),
        "location": "Винный погреб «Берег», ул. Крутая, 4",
        "price": 2200,
        "duration": 90,
        "category": "gastronomy",
        "image": IMG["wine"],
    },
    {
        "organizer": "elena.tours@turistpro.ru",
        "title": "Кулинарный мастер-класс: пельмени",
        "description": (
            "Готовим традиционные пельмени с нуля: тесто, начинка, лепка. "
            "Дегустация с чаем по завершении."
        ),
        "location": "Кулинарная студия «Вкус дома»",
        "price": 1900,
        "duration": 120,
        "category": "gastronomy",
        "image": IMG["cooking"],
    },
    {
        "organizer": "art.studio@turistpro.ru",
        "title": "Мастер-класс по гончарному делу",
        "description": (
            "Создайте свою чашу на гончарном круге под руководством мастера. "
            "Изделие можно забрать через 3 дня после обжига."
        ),
        "location": "Мастерская «Глина», ул. Художников, 7",
        "price": 2500,
        "duration": 120,
        "category": "masterclass",
        "image": IMG["pottery"],
    },
    {
        "organizer": "art.studio@turistpro.ru",
        "title": "Вечерняя фотопрогулка",
        "description": (
            "Мастер-класс по городской фотографии на закате: композиция, "
            "работа со светом, практика на 4 локациях."
        ),
        "location": "Смотровая площадка, парк Победы",
        "price": 2000,
        "duration": 90,
        "category": "masterclass",
        "image": IMG["photo"],
    },
    {
        "organizer": "art.studio@turistpro.ru",
        "title": "Театральная экскурсия за кулисы",
        "description": (
            "Уникальный доступ за кулисы городского театра: декорации, "
            "костюмерная, репетиционный зал. Мини-спектакль в финале."
        ),
        "location": "Городской драматический театр",
        "price": 1400,
        "duration": 80,
        "category": "history",
        "image": IMG["theater"],
    },
    {
        "organizer": "organizer@turistpro.ru",
        "title": "Речная прогулка на теплоходе",
        "description": (
            "Часовая прогулка по реке с аудиогидом. Панорама города с воды, "
            "фото-остановки у главных мостов."
        ),
        "location": "Причал «Южный», набережная 12",
        "price": 1100,
        "duration": 60,
        "category": "excursion",
        "image": IMG["river"],
    },
    {
        "organizer": "organizer@turistpro.ru",
        "title": "Музей городской истории",
        "description": (
            "Экскурсия по экспозиции с экспертом: от основания города до современности. "
            "Интерактивные залы и макеты."
        ),
        "location": "Музей истории, ул. Музейная, 2",
        "price": 800,
        "duration": 75,
        "category": "history",
        "image": IMG["museum"],
    },
]


def _user(email, full_name, phone, role, password):
    u = User(email=email, full_name=full_name, phone=phone, role=role)
    u.set_password(password)
    return u


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        for name, slug in CATEGORIES:
            db.session.add(Category(name=name, slug=slug))
        db.session.flush()

        users_by_email = {}
        for email, name, phone, role, pwd in ACCOUNTS:
            user = _user(email, name, phone, role, pwd)
            db.session.add(user)
            users_by_email[email] = user
        db.session.flush()

        slug_to_cat = {c.slug: c for c in Category.query.all()}
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        base_date = now.replace(hour=10, minute=0, second=0, microsecond=0)

        all_schedules = []
        for i, data in enumerate(ACTIVITIES):
            organizer = users_by_email[data["organizer"]]
            activity = Activity(
                title=data["title"],
                description=data["description"],
                location=data["location"],
                price=data["price"],
                duration_minutes=data["duration"],
                image_url=data["image"],
                category_id=slug_to_cat[data["category"]].id,
                organizer_id=organizer.id,
                is_active=True,
            )
            db.session.add(activity)
            db.session.flush()

            for day_offset in range(1, 5):
                schedule = Schedule(
                    activity_id=activity.id,
                    start_datetime=base_date
                    + timedelta(days=day_offset + (i % 3), hours=(day_offset % 3) * 3),
                    seats_total=20 if i % 2 == 0 else 12,
                    seats_booked=0,
                )
                db.session.add(schedule)
                all_schedules.append(schedule)

        db.session.flush()

        # Примеры оплаченных бронирований для демонстрации
        demo_bookings = [
            ("tourist@turistpro.ru", 0, 2),
            ("dmitry@turistpro.ru", 2, 1),
            ("anna@turistpro.ru", 5, 3),
        ]
        for tourist_email, sched_idx, seats in demo_bookings:
            schedule = all_schedules[sched_idx]
            tourist = users_by_email[tourist_email]
            amount = schedule.activity.price * seats
            schedule.seats_booked += seats
            booking = Booking(
                user_id=tourist.id,
                schedule_id=schedule.id,
                seats_count=seats,
                total_amount=amount,
                status=BookingStatus.PAID,
            )
            db.session.add(booking)
            db.session.flush()
            payment = Payment(
                booking_id=booking.id,
                amount=amount,
                status=PaymentStatus.SUCCESS,
                card_last4="4242",
                paid_at=now,
            )
            db.session.add(payment)

        db.session.commit()

        print("=" * 50)
        print("База заполнена тестовыми данными")
        print(f"  Категорий: {len(CATEGORIES)}")
        print(f"  Аккаунтов: {len(ACCOUNTS)}")
        print(f"  Мероприятий: {len(ACTIVITIES)} (все с изображениями)")
        print(f"  Слотов расписания: {len(all_schedules)}")
        print(f"  Демо-бронирований: {len(demo_bookings)}")
        print("=" * 50)
        print("\nТЕСТОВЫЕ АККАУНТЫ (пароль одинаковый в группе):\n")
        print("--- Администратор ---")
        print("  admin@turistpro.ru          / admin123")
        print("\n--- Организаторы (пароль: organizer123) ---")
        print("  organizer@turistpro.ru      / Иван Петров")
        print("  elena.tours@turistpro.ru    / Елена Смирнова (гастрономия)")
        print("  art.studio@turistpro.ru     / Алексей Кузнецов (мастер-классы)")
        print("\n--- Туристы (пароль: tourist123) ---")
        print("  tourist@turistpro.ru        / Мария Иванова")
        print("  dmitry@turistpro.ru         / Дмитрий Волков")
        print("  anna@turistpro.ru           / Анна Соколова")
        print("  guest.demo@turistpro.ru     / Олег Новиков")
        print("=" * 50)


if __name__ == "__main__":
    seed()
