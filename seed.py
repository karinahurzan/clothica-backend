import json
from app.database import SessionLocal
from app.models import Category, Good, Feedback


def seed_data():
    db = SessionLocal()

    try:
        # 1. Імпорт категорій
        with open("goods.categories.json", "r", encoding="utf-8") as f:
            categories_data = json.load(f)
            for cat in categories_data:
                cat_id = cat["_id"]["$oid"]
                if not db.query(Category).filter(Category.id == cat_id).first():
                    db.add(Category(id=cat_id, name=cat["name"]))
        db.commit()
        print("✅ Категорії імпортовані")

        # 2. Імпорт товарів
        with open("goods.goods.json", "r", encoding="utf-8") as f:
            goods_data = json.load(f)
            for g in goods_data:
                good_id = g["_id"]["$oid"]
                if not db.query(Good).filter(Good.id == good_id).first():
                    db.add(
                        Good(
                            id=good_id,
                            name=g["name"],
                            category_id=g["category"]["$oid"],
                            image=g["image"],
                            price_value=g["price"]["value"],
                            price_currency=g["price"]["currency"],
                            size=g["size"],
                            description=g["description"],
                            prevDescription=g.get("prevDescription"),
                            gender=g["gender"],
                            characteristics=g["characteristics"],
                        )
                    )
        db.commit()
        print("✅ Товари імпортовані")

        # 3. Імпорт відгуків (з перевіркою існування товару)
        with open("goods.feedbacks.json", "r", encoding="utf-8") as f:
            feedbacks_data = json.load(f)
            fb_count = 0
            for fb in feedbacks_data:
                fb_id = fb["_id"]["$oid"]
                product_id = fb["productId"]["$oid"]

                # Перевіряємо, чи є такий товар у базі
                product_exists = db.query(Good).filter(Good.id == product_id).first()

                if product_exists:
                    if not db.query(Feedback).filter(Feedback.id == fb_id).first():
                        db.add(
                            Feedback(
                                id=fb_id,
                                author=fb["author"],
                                date=fb["date"],
                                description=fb["description"],
                                rate=fb["rate"],
                                product_id=product_id,
                            )
                        )
                        fb_count += 1
                else:
                    # Просто ігноруємо відгук, якщо товару не існує
                    continue

        db.commit()
        print(f"✅ Відгуки імпортовані (додано: {fb_count})")

    except Exception as e:
        db.rollback()
        print(f"❌ Помилка під час імпорту: {e}")
    finally:
        db.close()
        print("🏁 Процес завершено")


if __name__ == "__main__":
    seed_data()
