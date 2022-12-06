import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# class Course(Base):
#     __tablename__ = "course"
#     id = sq.Column(sq.Integer, primary_key=True)
#     name = sq.Column(sq.String(length=40), unique=True)
    
#     def __str__(self):
#         return f'Course: {self.id}: {self.name}'
    
#     #homeworks = relationship("Homework", back_populates="course")
    
# class Homework(Base):
#     __tablename__="homework"
    
#     id = sq.Column(sq.Integer, primary_key=True)
#     number = sq.Column(sq.Integer, nullable=False)
#     description=sq.Column(sq.Text, nullable=False)
#     course_id=sq.Column(sq.Integer, sq.ForeignKey("course.id"), nullable=False)
    
#     # course= relationship(Course, back_populates="homeworks")
    
#     course = relationship(Course, backref="homeworks")
    
#     def __str__(self):
#         return f'Homework: {self.id}: ({self.number}, {self.description}, {self.course_id})'
    
    

class User(Base):
    __tablename__ = "user"
    id = sq.Column(sq.Integer, primary_key=True)
    token = sq.Column(sq.Text, nullable=False, unique=True)

class Candidate(Base):
    __tablename__ = "candidate"
    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.Text, nullable=False)
    second_name = sq.Column(sq.Text, nullable=False)
    screen_name = sq.Column(sq.Text, nullable=False)




def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)