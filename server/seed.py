# server/seed.py
from app import app, db
from models import Customer, Item, Review

with app.app_context():
    print("Clearing old data...")
    Review.query.delete()
    Item.query.delete()
    Customer.query.delete()

    print("Seeding customers...")
    c1 = Customer(name="Alice")
    c2 = Customer(name="Bob")
    c3 = Customer(name="Charlie")

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    print("Seeding items...")
    i1 = Item(name="Laptop", price=1200.00)
    i2 = Item(name="Phone", price=800.00)
    i3 = Item(name="Headphones", price=150.00)

    db.session.add_all([i1, i2, i3])
    db.session.commit()

    print("Seeding reviews...")
    r1 = Review(comment="Great laptop, very fast!", customer=c1, item=i1)
    r2 = Review(comment="Phone battery could be better.", customer=c2, item=i2)
    r3 = Review(comment="Love these headphones, great sound!", customer=c3, item=i3)
    r4 = Review(comment="Alice also bought headphones.", customer=c1, item=i3)

    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()

    print("✅ Done seeding!")
