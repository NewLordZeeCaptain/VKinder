from random import randrange
import sqlalchemy as sq
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from functions.user_functions import User as Usr
from db.models import User, DatingUser, BlackList, Photos, Base


# Подключение к БД


# engine = sq.create_engine(CONSTR)
# Session = sessionmaker(bind=engine)


""" 
ФУНКЦИИ РАБОТЫ С БД
"""


class DB(object):
    """This object is used to interact with DB functions"""

    def __init__(self, CONSTR, USER_TOKEN):
        super(DB, self).__init__()

        engine = sq.create_engine(CONSTR)
        Session = sessionmaker(engine)
        self.session = Session()

        self.user = Usr(USER_TOKEN)

        Base.metadata.create_all(engine)

    def delete_db_blacklist(self, ids):
        current_user = session.query(BlackList).filter_by(vk_id=ids).first()
        if current_user:
            self.session.delete(current_user)
            self.session.commit()
            return True
        else:
            return False

    def delete_db_favorites(self, ids):
        current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
        if current_user:
            self.session.delete(current_user)
            self.session.commit()
            return True
        else:
            return False

    def check_db_master(self, ids):
        pass

    def check_db_user(self, ids):
        pass

    def search_user(self):
        pass

    def register_user(self, ids):
        user = self.session.query(User).filter_by(vk_id=ids).first()
        if user == None:
            self.session.add(User(vk_id=ids))
            self.session.commit()

    def check_db_blacklist(self, ids):
        current_user = self.session.query(User).filter_by(vk_id=ids).first()
        all_users = (
            self.session.query(BlackList).filter_by(id_user=current_user.id).all()
        )

        if all_users != []:
            user_dict = dict()
            for k, v in enumerate(all_users):
                user_dict[k] = v
            return user_dict

        else:
            return "Пусто, попробуйте для начала выполнить поиск и кого-нибудь добавить"

    def check_db_favorites(self, ids):
        current_user = self.session.query(User).filter_by(vk_id=ids).first()
        all_users = (
            self.session.query(DatingUser).filter_by(id_user=current_user.id).all()
        )
        print(all_users)
        if all_users != []:
            user_dict = dict()
            for k, v in enumerate(all_users):
                user_dict[k] = v
            return user_dict
        else:
            return "Никого нет, попробуйте для начала выполнить поиск и кого-нибудь добавить"

    def add_to_blacklist(self, user_id, vk_id):
        user = self.session.query(BlackList).filter_by(vk_id=vk_id).first()
        if user == None:
            result = self.user.user_get(vk_id)
            photo = self.user.get_photo(vk_id)[0]

            self.session.add(
                BlackList(
                    vk_id=result["id"],
                    first_name=result["first_name"],
                    second_name=result["last_name"],
                    city=result["city"],
                    link_photo=photo[1],
                    count_likes=photo[0],
                    user_id=user_id,
                )
            )
            return True
            self.session.commit()
            # pprint(self.user.get_photo(vk_id))
        else:
            return False

    def add_user(self, user_id, vk_id, first_name, last_name, city):
        user = (
            self.session.query(DatingUser)
            .filter_by(user_id=user_id, vk_id=vk_id)
            .first()
        )
        if user == None:
            
            photo = self.user.get_photo(vk_id)[0]
            self.session.add(
                DatingUser(
                    vk_id=vk_id,
                    first_name=first_name,
                    second_name=last_name,
                    city=city,
                    link="https://vk.com/id"+vk_id,
                    user_id=user_id,
                )
            )
            self.session.add()
            return True
        else:
            return False

    def add_user_photos(self, vk_id):
        user = self.session.query(Photos).filter_by(vk_id=vk_id).first()
        if user == None:
            for photo in self.user.get_photo(vk_id)[0:3]:
                self.session.add(
                    Photos(
                        link_photo=photo[1],
                        count_likes=photo[0],
                        id_dating_user=vk_id,
                    )
                )
            return True
        else:
            return False

            


# # проверят есть ли юзер в бд
# def check_db_user(ids):
#     dating_user = session.query(DatingUser).filter_by(vk_id=ids).first()
#     blocked_user = session.query(BlackList).filter_by(vk_id=ids).first()
#     return dating_user, blocked_user
