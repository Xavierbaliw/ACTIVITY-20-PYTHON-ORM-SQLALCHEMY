from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URI = 'sqlite:///ORMEventManagementDb.db'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True)
    admin_username = Column(String)
    admin_email = Column(String)
    admin_password = Column(String)

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_gmail = Column(String)
    user_password = Column(String)
    user_lastname = Column(String)

class Events(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_title = Column(String)
    event_description = Column(String)
    event_additional_description = Column(Text)
    event_address = Column(String)
    event_planner = Column(String)
    event_image = Column(String)
    event_status = Column(String)
    event_start = Column(Date)

class Agenda(Base):
    __tablename__ = 'agenda'
    agenda_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    agenda_time_start = Column(String)
    agenda_time_end = Column(String)

class Attendees(Base):
    __tablename__ = 'attendees'
    attendees_id = Column(Integer, primary_key=True)
    invitation_id = Column(Integer, ForeignKey('invited.invitation_id'))

class Invited(Base):
    __tablename__ = 'invited'
    invitation_id = Column(Integer, primary_key=True)
    invitation_name = Column(String)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    attendee_type = Column(String)
    seat_number = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

admin_data = [
    Admin(admin_id=1, admin_username='admin1', admin_email='admin1@gmail.com', admin_password='adminpass1'),
    Admin(admin_id=2, admin_username='admin2', admin_email='admin2@gmail.com', admin_password='adminpass2'),
    Admin(admin_id=3, admin_username='admin3', admin_email='admin3@gmail.com', admin_password='adminpass3'),
    Admin(admin_id=4, admin_username='admin4', admin_email='admin4@gmail.com', admin_password='adminpass4'),
    Admin(admin_id=5, admin_username='admin5', admin_email='admin5@gmail.com', admin_password='adminpass5'),
]

user_data = [
    User(user_id=1, user_gmail='Xavier@gmail.com', user_password='password1', user_lastname='Avelino'),
    User(user_id=2, user_gmail='Taay@gmail.com', user_password='password2', user_lastname='James'),
    User(user_id=3, user_gmail='Walter@gmail.com', user_password='password3', user_lastname='Curry'),
    User(user_id=4, user_gmail='Fierci@gmail.com', user_password='password4', user_lastname='Mark'),
    User(user_id=5, user_gmail='Cano@gmail.com', user_password='password5', user_lastname='Roerenz'),
]

event_data = [
    Events(event_id=1, event_title='Harvest Festival 2023', event_description='Celebrate the bountiful harvest with food, fun, and family activities!', event_additional_description='Join us for an unforgettable day filled with local produce, craft vendors, live music, and childrens activities', event_address='123 Farm Lane, Springfield, IL 62701', event_planner='Planner One', event_image='image1.jpg', event_status='active', event_start=datetime.strptime('2023-11-01', '%Y-%m-%d').date()),
    Events(event_id=2, event_title='Tech Innovation Summit', event_description='Explore the latest trends in technology and entrepreneurship.', event_additional_description='This summit gathers industry leaders, startups, and innovators to discuss the future of technology.', event_address='456 Tech Ave, Silicon Valley, CA 94043', event_planner='Planner Two', event_image='image2.jpg', event_status='active', event_start=datetime.strptime('2023-11-02', '%Y-%m-%d').date()),
    Events(event_id=3, event_title='Art in the Park', event_description='An outdoor art exhibition featuring local artists.', event_additional_description='Come and enjoy a day of creativity and inspiration at our annual Art in the Park! Browse art installations, enjoy live music, and meet local artists.', event_address='City Park, 789 Art St, Denver, CO 80204', event_planner='Planner Three', event_image='image3.jpg', event_status='active', event_start=datetime.strptime('2023-11-03', '%Y-%m-%d').date()),
    Events(event_id=4, event_title='Mindfulness Meditation Retreat', event_description='A weekend retreat to relax and rejuvenate your mind and body.', event_additional_description='Escape the hustle and bustle of daily life at our Mindfulness Meditation Retreat.', event_address='Serenity Hills Lodge, 234 Tranquil Rd, Asheville, NC 28801', event_planner='Planner Four', event_image='image4.jpg', event_status='active', event_start=datetime.strptime('2023-11-04', '%Y-%m-%d').date()),
    Events(event_id=5, event_title='Music Under the Stars', event_description='A night of live music and community spirit under the stars.', event_additional_description='Gather your friends and family for an evening of live performances from local bands.', event_address='Starry Park, 345 Rhythm Ln, Nashville, TN 37201', event_planner='Planner Five', event_image='image5.jpg', event_status='active', event_start=datetime.strptime('2023-11-05', '%Y-%m-%d').date()),
]

agenda_data = [
    Agenda(agenda_id=1, event_id=1, agenda_time_start='10:00', agenda_time_end='11:00'),
    Agenda(agenda_id=2, event_id=2, agenda_time_start='11:00', agenda_time_end='12:00'),
    Agenda(agenda_id=3, event_id=3, agenda_time_start='12:00', agenda_time_end='13:00'),
    Agenda(agenda_id=4, event_id=4, agenda_time_start='13:00', agenda_time_end='14:00'),
    Agenda(agenda_id=5, event_id=5, agenda_time_start='14:00', agenda_time_end='15:00'),
]

attendee_data = [
    Attendees(attendees_id=1, invitation_id=1),
    Attendees(attendees_id=2, invitation_id=2),
    Attendees(attendees_id=3, invitation_id=3),
    Attendees(attendees_id=4, invitation_id=4),
    Attendees(attendees_id=5, invitation_id=5),
]

invited_data = [
    Invited(invitation_id=1, invitation_name='Xavier', event_id=1, attendee_type='VIP', seat_number='A1'),
    Invited(invitation_id=2, invitation_name='Taay', event_id=2, attendee_type='Regular', seat_number='B1'),
    Invited(invitation_id=3, invitation_name='Walter', event_id=3, attendee_type='VIP', seat_number='C1'),
    Invited(invitation_id=4, invitation_name='Fierci', event_id=4, attendee_type='Regular', seat_number='D1'),
    Invited(invitation_id=5, invitation_name='Cano', event_id=5, attendee_type='VIP', seat_number='E1'),
]

session.add_all(admin_data)
session.add_all(user_data)
session.add_all(event_data)
session.add_all(agenda_data)
session.add_all(attendee_data)
session.add_all(invited_data)

session.commit()
session.close()