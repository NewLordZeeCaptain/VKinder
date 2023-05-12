from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sq

Base = declarative_base()


# Пользователь бота ВК
class User(Base):
    __tablename__ = "user"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)


class Favorite(Base):
    __tablename__ = "favorite"
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


class Blacklist(Base):
    __tablename__ = "blacklist"
    vk_id = sq.Column(sq.Integer, unique=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


# Анкеты добавленные в избранное
# class DatingUser(Base):
#     __tablename__ = "dating_user"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.Integer, unique=True)
#     first_name = sq.Column(sq.String)
#     second_name = sq.Column(sq.String)
#     city = sq.Column(sq.Integer)
#     link = sq.Column(sq.String)
#     user_id = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))


# # Фото избранных анкет
# class Photos(Base):
#     __tablename__ = "photos"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     link_photo = sq.Column(sq.String)
#     count_likes = sq.Column(sq.Integer)
#     id_dating_user = sq.Column(
#         sq.Integer, sq.ForeignKey("dating_user.id", ondelete="CASCADE")
#     )


# # Анкеты в черном списке
# class BlackList(Base):
#     __tablename__ = "black_list"
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.Integer, unique=True)
#     first_name = sq.Column(sq.String)
#     second_name = sq.Column(sq.String)
#     city = sq.Column(sq.Integer)
#     link = sq.Column(sq.String)
#     link_photo = sq.Column(sq.String)
#     count_likes = sq.Column(sq.Integer)
#     id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id", ondelete="CASCADE"))
