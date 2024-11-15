from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Enum, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from datetime import timezone

DATABASE_URI = 'sqlite:///ORMTravelBookingDb.db'
engine = create_engine(DATABASE_URI, echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password_hash = Column(String(255))
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
    first_name = Column(String(50))
    last_name = Column(String(50))
    user_role = Column(Enum('ADMIN', 'USERS'))
    created_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(timezone.utc), onupdate=datetime.datetime.now(timezone.utc))
    deleted_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))


class Tour(Base):
    __tablename__ = 'tours'
    tour_id = Column(Integer, primary_key=True)
    tour_name = Column(String)
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    seats_available = Column(Integer)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(timezone.utc), onupdate=datetime.datetime.now(timezone.utc))
    deleted_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))


class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.now(timezone.utc))
    amount = Column(DECIMAL(10, 2))
    payment_method = Column(Enum('GCASH'))
    payment_status = Column(Enum('SUCCESS', 'FAILED'))
    transaction_id = Column(String(100))


class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    tour_id = Column(Integer, ForeignKey('tours.tour_id'), nullable=False)
    booking_date = Column(DateTime, default=datetime.datetime.now(timezone.utc))
    travel_date = Column(Date)
    seats_booked = Column(Integer)
    total_amount = Column(DECIMAL(10, 2))
    payment_status = Column(Enum('SUCCESS', 'FAILED'))
    created_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(timezone.utc), onupdate=datetime.datetime.now(timezone.utc))


class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    tour_id = Column(Integer, ForeignKey('tours.tour_id'), nullable=False)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))


class AdminLog(Base):
    __tablename__ = 'admin_logs'
    log_id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    action_type = Column(Enum('CREATE', 'UPDATE', 'DELETE'))
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.now(timezone.utc))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


user_data = [
    User(username='xavier14', password_hash='hashed_password1', email='xavier@gmail.com', phone_number='09933214290', first_name='Xavier', last_name='Avelino', user_role='ADMIN'),
    User(username='fierci26', password_hash='hashed_password2', email='fierci@gmail.com', phone_number='09933214291', first_name='Fercival', last_name='Adawe', user_role='USERS'),
    User(username='roerenz69', password_hash='hashed_password3', email='roerenz@gmail.com', phone_number='09933214292', first_name='Roerenz', last_name='Cano', user_role='ADMIN'),
    User(username='rodney04', password_hash='hashed_password4', email='rodney@gmail.com', phone_number='09933214293', first_name='Rodney', last_name='Idanan', user_role='USERS'),
    User(username='james12', password_hash='hashed_password5', email='james@gmail.com', phone_number='09933214294', first_name='James', last_name='Taay', user_role='USERS')
]


session.add_all(user_data)
session.commit()


tour_data = [
    Tour(tour_name='City Tour', description='Explore the city attractions.', price=50.00, start_date=datetime.date(2023, 12, 1), end_date=datetime.date(2023, 12, 31), seats_available=10, image_url='image1.jpg'),
    Tour(tour_name='Mountain Trek', description='Hike through the mountains.', price=75.00, start_date=datetime.date(2023, 11, 1), end_date=datetime.date(2023, 11, 15), seats_available=5, image_url='image2.jpg'),
    Tour(tour_name='Beach Getaway', description='Relax at the sunny beach.', price=100.00, start_date=datetime.date(2023, 11, 10), end_date=datetime.date(2023, 11, 20), seats_available=20, image_url='image3.jpg'),
    Tour(tour_name='Historical Sites', description='Visit ancient historical sites.', price=60.00, start_date=datetime.date(2023, 12, 5), end_date=datetime.date(2023, 12, 25), seats_available=15, image_url='image4.jpg'),
    Tour(tour_name='Wildlife Safari', description='Experience wildlife up close.', price=120.00, start_date=datetime.date(2023, 12, 10), end_date=datetime.date(2023, 12, 20), seats_available=8, image_url='image5.jpg')
]


session.add_all(tour_data)
session.commit()


booking_data = [
    Booking(user_id=1, tour_id=1, travel_date=datetime.date(2023, 12, 15), seats_booked=2, total_amount=100.00, payment_status='SUCCESS'),
    Booking(user_id=2, tour_id=2, travel_date=datetime.date(2023, 11, 10), seats_booked=1, total_amount=75.00, payment_status='SUCCESS'),
    Booking(user_id=3, tour_id=3, travel_date=datetime.date(2023, 11, 20), seats_booked=3, total_amount=300.00, payment_status='FAILED'),
    Booking(user_id=4, tour_id=4, travel_date=datetime.date(2023, 12, 10), seats_booked=4, total_amount=240.00, payment_status='SUCCESS'),
    Booking(user_id=5, tour_id=5, travel_date=datetime.date(2023, 12, 12), seats_booked=2, total_amount=240.00, payment_status='SUCCESS')
]


session.add_all(booking_data)
session.commit()


payment_data = [
    Payment(booking_id=1, amount=100.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TRANS001'),
    Payment(booking_id=2, amount=75.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TRANS002'),
    # Adjust booking_id to match those added above, and ensure they exist.
    Payment(booking_id=3, amount=300.00, payment_method='GCASH', payment_status='FAILED', transaction_id='TRANS003'),
    Payment(booking_id=4, amount=240.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TRANS004'),
    Payment(booking_id=5, amount=240.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TRANS005')
]


session.add_all(payment_data)
session.commit()


review_data = [
    Review(user_id=1, tour_id=1, rating=5, comment='Great tour!'),
    Review(user_id=2, tour_id=2, rating=4, comment='Enjoyed the trek!'),
    Review(user_id=3, tour_id=3, rating=3, comment='It was okay.'),
    Review(user_id=4, tour_id=4, rating=5, comment='Loved the history!'),
    Review(user_id=5, tour_id=5, rating=5, comment='Amazing experience!')
]


session.add_all(review_data)
session.commit()


admin_log_data = [
    AdminLog(admin_id=3, action_type='CREATE', description='Created a new tour.'),
    AdminLog(admin_id=3, action_type='UPDATE', description='Updated tour prices.'),
    AdminLog(admin_id=3, action_type='DELETE', description='Deleted a tour.'),
    AdminLog(admin_id=3, action_type='CREATE', description='Created a new booking.'),
    AdminLog(admin_id=3, action_type='CREATE', description='Created a new user.')
]


session.add_all(admin_log_data)
session.commit()


session.close()