import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.Text)
    last_name = sqlalchemy.Column(sqlalchemy.Text)
    gender = sqlalchemy.Column(sqlalchemy.Text)
    email = sqlalchemy.Column(sqlalchemy.Text)
    birthdate = sqlalchemy.Column(sqlalchemy.Text)
    height = sqlalchemy.Column(sqlalchemy.Float)


class Athelete(Base):
    __tablename__ = "athelete"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    birthdate = sqlalchemy.Column(sqlalchemy.Text)
    gender = sqlalchemy.Column(sqlalchemy.Text)
    height = sqlalchemy.Column(sqlalchemy.Float)
    name = sqlalchemy.Column(sqlalchemy.Text)
    weight = sqlalchemy.Column(sqlalchemy.Integer)
    gold_medals = sqlalchemy.Column(sqlalchemy.Integer)
    silver_medals = sqlalchemy.Column(sqlalchemy.Integer)
    bronze_medals = sqlalchemy.Column(sqlalchemy.Integer)
    total_medals = sqlalchemy.Column(sqlalchemy.Integer)
    sport = sqlalchemy.Column(sqlalchemy.Text)
    country = sqlalchemy.Column(sqlalchemy.Text)


def connect_db():
    engine = sqlalchemy.create_engine(DATABASE)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_id():
    id = input("Введите id: ")
    return id


def string_to_date(user):
    temp = user.birthdate.split("-")
    date = map(int, temp)
    date = datetime.date(*date)

    return date


def find_nearest_birthbay_athelete(user):
    session = connect_db()

    all_atheletes = session.query(Athelete).all()
    athelete_dict = {}

    for athelete in all_atheletes:
        date = string_to_date(athelete)
        athelete_dict.update({athelete.id : date})

    athelete_id = None
    min_delta = None
    user_birthdate = string_to_date(user)

    for key, val in athelete_dict.items():
        delta = abs(user_birthdate - val)
        if not min_delta or min_delta > delta:
            min_delta = delta
            athelete_id = key

    return athelete_id


def find_nearest_height_athelete(user):
    session = connect_db()

    all_atheletes = session.query(Athelete).filter(Athelete.height != None).all()
    athelete_dict = {}

    for athelete in all_atheletes:
        athelete_dict.update({athelete.id : athelete.height})

    user_height = user.height
    athelete_id = None
    min_delta = 100

    for key, val in athelete_dict.items():
        delta = abs(user_height - val)
        if min_delta > delta:
            min_delta = delta
            athelete_id = key

    return athelete_id


def main():
    id = request_id()
    if not id.isdigit():
        print("id должен быть числом")

    session = connect_db()

    q = session.query(User).filter(User.id == id).first()

    if q:
        near_height = find_nearest_height_athelete(q)
        near_birthdate = find_nearest_birthbay_athelete(q)
    else:
        print("Нет такого пользователя!!!")

    print("Ближайший по росту атлет: ", near_height)
    print("Ближайший по дате рождения атлет: ", near_birthdate)


if __name__ == "__main__":
    main()