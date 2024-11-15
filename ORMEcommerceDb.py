from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    password = Column(String)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    sku = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    price = Column(Float)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    total_amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

engine = create_engine('sqlite:///ORMEcommerceDb.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    User(password='pass1', name='Alice', address='123 Main St', phone='1234567890', role='customer'),
    User(password='pass2', name='Bob', address='456 Elm St', phone='0987654321', role='seller'),
    User(password='pass3', name='Charlie', address='789 Maple St', phone='5432167890', role='customer'),
    User(password='pass4', name='Diana', address='321 Oak St', phone='4567890123', role='admin'),
    User(password='pass5', name='Ethan', address='654 Pine St', phone='6789012345', role='customer'),

    Product(name='Laptop', brand='BrandA', description='Gaming Laptop', price=1200.00, stock=10,
            category='Electronics', sku='LAP123', image_url='https://example.com/laptop.jpg'),
    Product(name='Phone', brand='BrandB', description='Smartphone', price=700.00, stock=20,
            category='Electronics', sku='PHO456', image_url='https://example.com/phone.jpg'),
    Product(name='Tablet', brand='BrandC', description='Android Tablet', price=300.00, stock=15,
            category='Electronics', sku='TAB789', image_url='https://example.com/tablet.jpg'),
    Product(name='Headphones', brand='BrandD', description='Wireless Headphones', price=150.00, stock=25,
            category='Electronics', sku='HEA012', image_url='https://example.com/headphones.jpg'),
    Product(name='Smartwatch', brand='BrandE', description='Fitness Tracker', price=200.00, stock=30,
            category='Electronics', sku='SMA345', image_url='https://example.com/smartwatch.jpg'),

    Review(user_id=1, product_id=1, rating=5, comment='Excellent laptop!'),
    Review(user_id=2, product_id=2, rating=4, comment='Very good phone.'),
    Review(user_id=3, product_id=3, rating=3, comment='Average tablet.'),
    Review(user_id=4, product_id=4, rating=5, comment='Love these headphones!'),
    Review(user_id=5, product_id=5, rating=4, comment='Great smartwatch.'),

    OrderItem(order_id=1, product_id=1, quantity=1, price=1200.00),
    OrderItem(order_id=1, product_id=2, quantity=2, price=1400.00),
    OrderItem(order_id=2, product_id=3, quantity=1, price=300.00),
    OrderItem(order_id=2, product_id=4, quantity=3, price=450.00),
    OrderItem(order_id=3, product_id=5, quantity=1, price=200.00),

    Order(user_id=1, total_amount=2800.00, status='Completed'),
    Order(user_id=3, total_amount=300.00, status='Pending'),
    Order(user_id=2, total_amount=450.00, status='Shipped'),
    Order(user_id=4, total_amount=150.00, status='Delivered'),
    Order(user_id=5, total_amount=200.00, status='Cancelled'),
])

session.commit()
session.close()