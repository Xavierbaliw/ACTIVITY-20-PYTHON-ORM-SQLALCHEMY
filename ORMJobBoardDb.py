from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    authentication_id = Column(Integer, ForeignKey('authentication.authentication_id'))
    name = Column(String)
    birthdate = Column(DateTime(timezone=True))
    skills = Column(Text)
    work_experience = Column(Text)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class Authentication(Base):
    __tablename__ = 'authentication'
    authentication_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    role = Column(Enum('admin', 'employer', 'job_seeker'))
    stock = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class Message(Base):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.user_id'))
    recipient_id = Column(Integer, ForeignKey('user.user_id'))
    message = Column(Text)
    is_read = Column(Boolean)
    message_type = Column(Enum('TEXT', 'IMAGE', 'FILE'))
    send_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class Applications(Base):
    __tablename__ = 'applications'
    application_id = Column(Integer, primary_key=True)
    job_seeker_id = Column(Integer, ForeignKey('user.user_id'))
    job_id = Column(Integer, ForeignKey('job_posting.job_id'))
    resume = Column(Text)
    status = Column(Enum('PENDING', 'ACCEPTED', 'REJECTED'))
    skills = Column(Text)
    work_experience = Column(Text)
    applied_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class JobPosting(Base):
    __tablename__ = 'job_posting'
    job_id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('user.user_id'))
    job_title = Column(String)
    job_description = Column(Text)
    location = Column(String)
    category = Column(String)
    industry = Column(String)
    min_salary = Column(Integer)
    max_salary = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class JobInteraction(Base):
    __tablename__ = 'job_interaction'
    interaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    job_id = Column(Integer, ForeignKey('job_posting.job_id'))
    interaction_type = Column(Integer)
    interaction_date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_applied = Column(Boolean)

engine = create_engine('sqlite:///ORMJobBoardDb.Db', connect_args={"check_same_thread": False})

# Ensure the database tables are created
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Adding data with correct datetime objects
session.add_all([
    User(user_id=1, authentication_id=1, name='Xavier', birthdate=datetime(1990, 1, 1, tzinfo=timezone.utc),
         skills='Python, SQL', work_experience='5 years'),
    User(user_id=2, authentication_id=2, name='Taay', birthdate=datetime(1988, 2, 1, tzinfo=timezone.utc),
         skills='Java, NoSQL', work_experience='7 years'),
    User(user_id=3, authentication_id=3, name='Walter', birthdate=datetime(1992, 3, 1, tzinfo=timezone.utc),
         skills='JavaScript, React', work_experience='4 years'),
    User(user_id=4, authentication_id=4, name='Fierci', birthdate=datetime(1985, 4, 1, tzinfo=timezone.utc),
         skills='HTML, CSS', work_experience='6 years'),
    User(user_id=5, authentication_id=5, name='Idanan', birthdate=datetime(1975, 5, 1, tzinfo=timezone.utc),
         skills='C++, C#', work_experience='10 years'),

    Authentication(authentication_id=1, username='Xavier', email='xavier@gmail.com', password_hash='hashedpw1',
                   role='job_seeker', stock=0),
    Authentication(authentication_id=2, username='Taay', email='taay@gmail.com', password_hash='hashedpw2',
                   role='employer', stock=0),
    Authentication(authentication_id=3, username='Walter', email='walter@gmail.com', password_hash='hashedpw3',
                   role='job_seeker', stock=0),
    Authentication(authentication_id=4, username='Fierci', email='fierci@gmail.com', password_hash='hashedpw4',
                   role='employer', stock=0),
    Authentication(authentication_id=5, username='Idanan', email='idanan@gmail.com', password_hash='hashedpw5',
                   role='job_seeker', stock=0),

    Message(message_id=1, sender_id=1, recipient_id=2, message='Hello!', is_read=False, message_type='TEXT'),
    Message(message_id=2, sender_id=2, recipient_id=3, message='Job opportunity for you!', is_read=False,
            message_type='TEXT'),
    Message(message_id=3, sender_id=3, recipient_id=4, message='Interested in the job!', is_read=True,
            message_type='TEXT'),
    Message(message_id=4, sender_id=4, recipient_id=5, message='Please send your resume.', is_read=False,
            message_type='TEXT'),
    Message(message_id=5, sender_id=5, recipient_id=1, message='Can we schedule an interview?', is_read=False,
            message_type='TEXT'),

    Applications(application_id=1, job_seeker_id=1, job_id=1, resume='Xavier_Resume.pdf', status='PENDING',
                 skills='Python', work_experience='5 years'),
    Applications(application_id=2, job_seeker_id=2, job_id=2, resume='Taay_Resume.pdf', status='ACCEPTED',
                 skills='Java', work_experience='7 years'),
    Applications(application_id=3, job_seeker_id=3, job_id=3, resume='Walter_Resume.pdf', status='REJECTED',
                 skills='JavaScript', work_experience='4 years'),
    Applications(application_id=4, job_seeker_id=4, job_id=4, resume='Fierci_Resume.pdf', status='PENDING',
                 skills='HTML', work_experience='6 years'),
    Applications(application_id=5, job_seeker_id=5, job_id=5, resume='Idanan_Resume.pdf', status='ACCEPTED',
                 skills='C++', work_experience='10 years'),

    JobPosting(job_id=1, employer_id=2, job_title='Python Developer',
               job_description='Develop applications using Python.', location='New York', category='IT',
               industry='Software', min_salary=70000, max_salary=100000),
    JobPosting(job_id=2, employer_id=4, job_title='Java Developer', job_description='Develop applications using Java.',
               location='San Francisco', category='IT', industry='Software', min_salary=80000, max_salary=120000),
    JobPosting(job_id=3, employer_id=2, job_title='Frontend Developer',
               job_description='Work on the UI of the application.', location='Austin', category='IT',
               industry='Software', min_salary=60000, max_salary=90000),
    JobPosting(job_id=4, employer_id=4, job_title='Full Stack Developer',
               job_description='Work on both frontend and backend.', location='Seattle', category='IT',
               industry='Software', min_salary=90000, max_salary=130000),
    JobPosting(job_id=5, employer_id=2, job_title='Data Scientist', job_description='Analyze data and create reports.',
               location='Chicago', category='IT', industry='Software', min_salary=80000, max_salary=110000),

    JobInteraction(interaction_id=1, user_id=1, job_id=1, interaction_type=1, interaction_date=datetime.now(timezone.utc),
                   is_applied=True),
    JobInteraction(interaction_id=2, user_id=2, job_id=2, interaction_type=1, interaction_date=datetime.now(timezone.utc),
                   is_applied=False),
    JobInteraction(interaction_id=3, user_id=3, job_id=3, interaction_type=1, interaction_date=datetime.now(timezone.utc),
                   is_applied=True),
    JobInteraction(interaction_id=4, user_id=4, job_id=4, interaction_type=1, interaction_date=datetime.now(timezone.utc),
                   is_applied=True),
    JobInteraction(interaction_id=5, user_id=5, job_id=5, interaction_type=1, interaction_date=datetime.now(timezone.utc),
                   is_applied=False)
])

session.commit()
session.close()