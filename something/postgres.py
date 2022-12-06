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

Homework(number=1, description="Simple HW", course=course1)
Homework(number=2, description="Hard HW", course=course1)
session.add_all()
session.commit()


session.close()