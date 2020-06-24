import sqlalchemy
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


def connect_db():
    engine = sqlalchemy.create_engine(DATABASE)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender: ")
    email = input("email: ")
    birthdate = input("Birthdate(YYYY-MM-DD): ")
    height = input("Height: ")


    user = User(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
    )

    return user


def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()

if __name__ == "__main__":
    main()