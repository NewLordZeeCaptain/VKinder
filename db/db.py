import sqlalchemy as sq

# from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from configs.config import CONSTR
from db.models import *


# Подключение к БД


    
Session = sessionmaker(bind=sq.create_engine(CONSTR))
Base.metadata.drop_all(sq.create_engine(CONSTR))
print("Drop DB")
Base.metadata.create_all(sq.create_engine(CONSTR))
print("Create DB")
session = Session()


""" 
ФУНКЦИИ РАБОТЫ С БД
"""


# class DB(object):
#     """This object is used to interact with DB functions"""

#     def __init__(self, CONSTR, USER_TOKEN):
#         super(DB, self).__init__()

#         engine = sq.create_engine(CONSTR)
#         Session = sessionmaker(engine)
#         self.session = Session()

#         self.user = Usr(USER_TOKEN)


def delete_db_blacklist(user_id, vk_id):
    current_user = session.query(User).filter_by(vk_id=user_id).first()
    user = (
        session.query(Blacklist).filter_by(vk_id=vk_id, user_id=current_user.id).first()
    )
    if current_user:
        session.delete(user)
        session.commit()
        return True
    else:
        return False


def delete_db_favorites(user_id, vk_id):
    current_user = session.query(User).filter_by(vk_id=user_id).first()
    user = (
        session.query(DatingUser)
        .filter_by(user_id=current_user.id, vk_id=vk_id)
        .first()
    )
    if user:
        session.delete(user)
        session.commit()
        return True
    else:
        return False


def register_user(user_id):
    user = session.query(User).filter_by(vk_id=user_id).first()
    if user == None:
        session.add(User(vk_id=user_id))
        session.commit()
        return True
    else:
        return False


def check_db_blacklist(user_id):
    current_user = session.query(User).filter_by(vk_id=user_id).first()
    all_users = session.query(Blacklist).filter_by(user_id=current_user.id).all()
    if all_users != []:
        user_dict = dict()
        for k, v in enumerate(all_users):
            user_dict[k] = v
        return user_dict
    else:
        return "Пусто, попробуйте для начала выполнить поиск и кого-нибудь добавить"


def check_db_favorites(user_id):
    current_user = session.query(User).filter_by(vk_id=user_id).first()
    all_users = session.query(Favorite).filter_by(user_id=current_user.id).all()
    if all_users != []:
        user_dict = dict()
        for k, v in enumerate(all_users):
            user_dict[k] = v
        return user_dict
    else:
        return (
            "Никого нет, попробуйте для начала выполнить поиск и кого-нибудь добавить"
        )


def add_to_blacklist(user_id, vk_id):
    current_user = session.query(User).filter_by(vk_id=user_id).first()
    user = session.query(Blacklist).filter_by(vk_id=vk_id).first()
    if user == None:
        session.add(
            Blacklist(
                vk_id=vk_id,
                user_id=current_user.id,
            )
        )
        return True
        session.commit()
        # pprint(self.user.get_photo(vk_id))
    else:
        return False


def add_user(user_id, vk_id):
    current_user = session.query(User).filter_by(vk_id=user_id).first()
    user = session.query(Favorite).filter_by(vk_id=vk_id, user_id=current_user.id)
    if user == None:
        session.add(Favorite(vk_id=vk_id, user_id=current_user.id))
        session.commit()
        return True
    else:
        return False
