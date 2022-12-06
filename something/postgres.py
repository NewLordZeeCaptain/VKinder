import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Course, Homework

DSN= 'postgresql://postgres:postgres@localhost:5432/vkinder_db'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine=engine)


Session = sessionmaker(bind=engine)

session = Session()

course1 = Course(name="Python")
print(course1.id)

session.add(course1)
session.commit()
print(course1)

hw1=Homework(number=1, description="Simple HW", course=course1)
hw2=Homework(number=2, description="Hard HW", course=course1)
session.add_all([hw1,hw2])
session.commit()

for c in session.query(Homework).filter(Homework.description.like('%Hard%')).all():
    print(c)

for c in session.query(Course).join(Homework.course).filter(Homework.number==2):
    print(c)

course2 = Course(name='Java')
session.add(course2)
session.commit()

subq = session.query(Homework).filter(Homework.description.like('%Har%')).subquery()
for c in session.query(Course).join(subq, Course.id ==  subq.c.course_id):
    print(c)

session.query(Course).filter(Course.name =="Java").update({'name': 'JavaScript'})
session.commit()

session.query(Course).filter(Course.name == "JavaScript").delete()
session.commit()

for c in session.query(Course).all():
    print(c)

session.close()