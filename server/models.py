# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# avoid Alembic naming issues
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    # allow creation without providing name (tests call Customer())
    name = db.Column(db.String, nullable=True, default=None)

    # One-to-many to Review
    reviews = db.relationship(
        "Review",
        back_populates="customer",
        cascade="all, delete-orphan",
        overlaps="items,customers"
    )

    # association proxy: customer.items -> through reviews.item
    # creator lets you do: customer.items.append(item)
    items = association_proxy(
        "reviews",
        "item",
        creator=lambda item_obj: Review(item=item_obj)
    )

    # avoid recursive serialization of relationships
    serialize_rules = ("-reviews.customer",)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True, default="Unnamed Item")
    price = db.Column(db.Float, nullable=True, default=0.0)

    reviews = db.relationship('Review', back_populates='item')
    customers = association_proxy('reviews', 'customer')

    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'



class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    customer = db.relationship(
        "Customer",
        back_populates="reviews",
        overlaps="items,customers"
    )
    item = db.relationship(
        "Item",
        back_populates="reviews",
        overlaps="items,customers"
    )

    serialize_rules = ("-customer.reviews", "-item.reviews")

    def __repr__(self):
        return f"<Review {self.id}, {self.comment}>"
