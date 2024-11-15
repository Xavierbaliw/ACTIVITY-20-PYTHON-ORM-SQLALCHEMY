from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, DateTime, Boolean, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum('teacher', 'student', name='user_roles'), nullable=False)
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Quiz(Base):
    __tablename__ = 'quiz'
    quiz_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    quiz_code = Column(String, unique=True)
    teacher_id = Column(Integer, ForeignKey('user.user_id'))
    duration = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    teacher = relationship("User")

class Question(Base):
    __tablename__ = 'question'
    question_id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum('MCQ', 'true or false', 'short answer', 'multimedia', name='question_types'))
    createdAt = Column(DateTime, default=datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Option(Base):
    __tablename__ = 'option'
    option_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.question_id'))
    option_text = Column(String, nullable=False)
    is_correct = Column(Boolean)

class Answer(Base):
    __tablename__ = 'answer'
    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.question_id'))
    student_id = Column(Integer, ForeignKey('user.user_id'))
    answer_text = Column(Text)
    submitted_At = Column(DateTime, default=datetime.now(timezone.utc))

class Result(Base):
    __tablename__ = 'result'
    result_id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    student_id = Column(Integer, ForeignKey('user.user_id'))
    score = Column(DECIMAL(5, 2))
    submitted_At = Column(DateTime, default=datetime.now(timezone.utc))

engine = create_engine('sqlite:///ORMQuizDb.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_dummy_data():
    users = [
        User(name='Alice', email='alice@example.com', password='password', role='student'),
        User(name='Bob', email='bob@example.com', password='password', role='teacher'),
        User(name='Charlie', email='charlie@example.com', password='password', role='student'),
        User(name='David', email='david@example.com', password='password', role='teacher'),
        User(name='Eve', email='eve@example.com', password='password', role='student')
    ]
    session.add_all(users)
    session.commit()

    quizzes = [
        Quiz(title='Math Quiz 1', description='Basic Math Quiz', quiz_code='MATH101', teacher_id=2, duration=30),
        Quiz(title='Science Quiz 1', description='Basic Science Quiz', quiz_code='SCI101', teacher_id=4, duration=30),
        Quiz(title='History Quiz 1', description='World History Quiz', quiz_code='HIST101', teacher_id=2, duration=30),
        Quiz(title='Geography Quiz 1', description='Geography Basics Quiz', quiz_code='GEOG101', teacher_id=4, duration=30),
        Quiz(title='Literature Quiz 1', description='Basic Literature Quiz', quiz_code='LIT101', teacher_id=2, duration=30),
    ]
    session.add_all(quizzes)
    session.commit()

    questions = [
        Question(quiz_id=1, question_text='What is 2 + 2?', question_type='MCQ'),
        Question(quiz_id=1, question_text='Is the Earth flat?', question_type='true or false'),
        Question(quiz_id=2, question_text='What is H2O commonly known as?', question_type='short answer'),
        Question(quiz_id=2, question_text='What is the capital of France?', question_type='MCQ'),
        Question(quiz_id=3, question_text='Who was the first President of the USA?', question_type='short answer'),
    ]
    session.add_all(questions)
    session.commit()

    options = [
        Option(question_id=1, option_text='3', is_correct=False),
        Option(question_id=1, option_text='4', is_correct=True),
        Option(question_id=1, option_text='5', is_correct=False),
        Option(question_id=2, option_text='True', is_correct=False),
        Option(question_id=2, option_text='False', is_correct=True),
        Option(question_id=4, option_text='London', is_correct=False),
        Option(question_id=4, option_text='Paris', is_correct=True),
        Option(question_id=4, option_text='Berlin', is_correct=False),
        Option(question_id=5, option_text='George Washington', is_correct=True),
        Option(question_id=5, option_text='Abraham Lincoln', is_correct=False),
    ]
    session.add_all(options)
    session.commit()

    answers = [
        Answer(question_id=1, student_id=1, answer_text='4'),
        Answer(question_id=2, student_id=3, answer_text='False'),
        Answer(question_id=3, student_id=1, answer_text='Water'),
        Answer(question_id=4, student_id=1, answer_text='Paris'),
        Answer(question_id=5, student_id=3, answer_text='George Washington')
    ]
    session.add_all(answers)
    session.commit()

    results = [
        Result(quiz_id=1, student_id=1, score=80.00),
        Result(quiz_id=2, student_id=3, score=90.00),
        Result(quiz_id=3, student_id=1, score=85.00),
        Result(quiz_id=4, student_id=2, score=75.00),
        Result(quiz_id=5, student_id=3, score=95.00)
    ]
    session.add_all(results)
    session.commit()

add_dummy_data()

def crud_example():
    print("All Users:")
    for user in session.query(User).all():
        print(user.name, user.email)

    user_to_update = session.query(User).filter_by(user_id=1).first()
    user_to_update.name = 'Alicia'
    session.commit()

    user_to_delete = session.query(User).filter_by(user_id=3).first()
    session.delete(user_to_delete)
    session.commit()

    print("\nUsers after update and delete:")
    for user in session.query(User).all():
        print(user.name, user.email)

crud_example()

session.close()