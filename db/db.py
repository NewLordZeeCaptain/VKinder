from random import randrange
import sqlalchemy as sq
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functions.user_functions import User as Usr

from configs.config import  CONSTR
from pprint import pprint

# Подключение к БД
Base = declarative_base()


# engine = sq.create_engine(CONSTR)
# Session = sessionmaker(bind=engine)




# Пользователь бота ВК
class User(Base):
    __tablename__ = "user"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)


# Анкеты добавленные в избранное
class DatingUser(Base):
    __tablename__ = "dating_user"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


# Фото избранных анкет
class Photos(Base):
    __tablename__ = "photos"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_dating_user = sq.Column(
        sq.Integer, sq.ForeignKey("dating_user.id", ondelete="CASCADE")
    )


# Анкеты в черном списке
class BlackList(Base):
    __tablename__ = "black_list"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


""" 
ФУНКЦИИ РАБОТЫ С БД
"""

class DB(object):
    """This object is used to interact with DB functions"""
    def __init__(self, CONSTR, USER_TOKEN):
        super(DB, self).__init__()
        
        engine = sq.create_engine(CONSTR)
        Session=sessionmaker(engine)
        self.session=Session()
        
        self.user = Usr(USER_TOKEN)
        
        
        Base.metadata.create_all(engine)
        

    def delete_db_blacklist(self,ids):
    
        current_user = session.query(BlackList).filter_by(vk_id=ids).first()
        self.session.delete(current_user)
        self.session.commit()
    
    def delete_db_favorites(self,ids):
        current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
        self.session.delete(current_user)
        self.session.commit()
        
    def check_db_master(self,ids):
        pass
    def check_db_user(self,ids):
        pass
    def register_user(self, ids):
        user = self.session.query(User).filter_by(vk_id=ids).first()
        if user == None:
            self.session.add(User(vk_id=ids)) 
            self.session.commit()
            
    def check_db_blacklist(self,ids):
        current_user = self.session.query(User).filter_by(vk_id=ids).first()
        all_users = self.session.query(BlackList).filter_by(id_user=current_user.id).all()
        return all_users
        


    def check_db_favorites(self,ids):
        current_user = self.session.query(User).filter_by(vk_id=ids).first()
        all_users = self.session.query(DatingUser).filter_by(id_user=current_user.id).all()
        return all_users
    
    def add_to_blacklist(self,user_id, vk_id):
        
        user = self.session.query(BlackList).filter_by(vk_id=vk_id).first()
        if user == None:
            result = self.user.user_get(vk_id)
            photo = self.user.get_photo(vk_id)[0]
            
            self.session.add(BlackList(
                vk_id=result['id'],
                first_name=result['first_name'],
                second_name=result['last_name'],
                city=result['city'],
                link_photo=photo[1],
                count_likes=photo[0],
                user_id=user_id
                
            )) 
            self.session.commit()
            # pprint(self.user.get_photo(vk_id))
            
    
    def add_user(self, vk_id):
        pass
    
    def add_user_photos(self, vk_id):
        pass


# Удаляет пользователя из черного списка
# def delete_db_blacklist(ids):
#     current_user = session.query(BlackList).filter_by(vk_id=ids).first()
#     session.delete(current_user)
#     session.commit()


# # Удаляет пользователя из избранного
# def delete_db_favorites(ids):
#     current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
#     session.delete(current_user)
#     session.commit()


# # проверят зареган ли пользователь бота в БД
# def check_db_master(ids):
#     current_user_id = session.query(User).filter_by(vk_id=ids).first()
#     return current_user_id


# # проверят есть ли юзер в бд
# def check_db_user(ids):
#     dating_user = session.query(DatingUser).filter_by(vk_id=ids).first()
#     blocked_user = session.query(BlackList).filter_by(vk_id=ids).first()
#     return dating_user, blocked_user


# # Проверят есть ли юзер в черном списке
# def check_db_black(ids):
#     current_users_id = session.query(User).filter_by(vk_id=ids).first()
#     # Находим все анкеты из избранного которые добавил данный юзер
#     all_users = session.query(BlackList).filter_by(id_user=current_users_id.id).all()
#     return all_users


# # Проверяет есть ли юзер в избранном
# def check_db_favorites(ids):
#     current_users_id = session.query(User).filter_by(vk_id=ids).first()
#     # Находим все анкеты из избранного которые добавил данный юзер
#     alls_users = session.query(DatingUser).filter_by(id_user=current_users_id.id).all()
#     return alls_users


# # Пишет сообщение пользователю


# def register_user(ids):
#     user = session.query(User).filter_by(vk_id=ids).first()
#     if user != None:
#         session.add(User(vk_id=ids))
#         session.commit()
    

# # Сохранение выбранного пользователя в БД
# def add_user(event_id, vk_id, first_name, second_name, city, link, id_user):
#     try:
#         new_user = DatingUser(
#             vk_id=vk_id,
#             first_name=first_name,
#             second_name=second_name,
#             city=city,
#             link=link,
#             id_user=id_user,
#         )
#         session.add(new_user)
#         session.commit()
#         write_msg(event_id, "ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ")
#         return True
#     except (IntegrityError, InvalidRequestError):
#         write_msg(event_id, "Пользователь уже в избранном.")
#         return False


# # Сохранение в БД фото добавленного пользователя
# def add_user_photos(event_id, link_photo, count_likes, id_dating_user):
#     try:
#         new_user = Photos(
#             link_photo=link_photo,
#             count_likes=count_likes,
#             id_dating_user=id_dating_user,
#         )
#         session.add(new_user)
#         session.commit()
#         write_msg(event_id, "Фото пользователя сохранено в избранном")
#         return True
#     except (IntegrityError, InvalidRequestError):
#         write_msg(
#             event_id, "Невозможно добавить фото этого пользователя(Уже сохранено)"
#         )
#         return False


# # Добавление пользователя в черный список
# def add_to_black_list(
#     event_id,
#     vk_id,
#     first_name,
#     second_name,
#     city,
#     link,
#     link_photo,
#     count_likes,
#     id_user,
# ):
#     try:
#         new_user = BlackList(
#             vk_id=vk_id,
#             first_name=first_name,
#             second_name=second_name,
#             city=city,
#             link=link,
#             link_photo=link_photo,
#             count_likes=count_likes,
#             id_user=id_user,
#         )
#         session.add(new_user)
#         session.commit()
#         write_msg(event_id, "Пользователь успешно заблокирован.")
#         return True
#     except (IntegrityError, InvalidRequestError):
#         write_msg(event_id, "Пользователь уже в черном списке.")
#         return False



