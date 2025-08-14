from sqlalchemy import Integer,String,Float,JSON,create_engine
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
s_engine = create_engine("postgresql+psycopg2://postgres:Auth-q09786@localhost:5432/usersdb", echo=True)
Base = declarative_base()
class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    user_username: Mapped[str] = mapped_column(String)
    user_lang: Mapped[str] = mapped_column(String)
    user_balance: Mapped[float] = mapped_column(Float,default=0)
    user_balance_max: Mapped[float] = mapped_column(Float,default=0)
    user_referral: Mapped[int] = mapped_column(Integer,default=0)
    user_profile_quantity: Mapped[int] = mapped_column(Integer,default=10)
    user_profile_quantity_subtraction: Mapped[int] = mapped_column(Integer,default=10)
    def __repr__(self):
        return f"<Users(user_id={self.user_id},user_username={self.user_username},user_lang={self.user_lang},user_balance={self.user_balance},user_balance_max={self.user_balance_max},user_referral={self.user_referral},user_profile_quantity={self.user_profile_quantity})>"
class ProfileSettings(Base):
    __tablename__ = 'Profile_Settings'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    profile_number: Mapped[int] = mapped_column(Integer,default=0)
    profile_settings: Mapped[dict] = mapped_column(JSON, default=dict)
    def __repr__(self):
        return f"<Profile_Settings(user_id={self.user_id},profile_number={self.profile_number},profile_settings={self.profile_settings})>"
default_settings = {
    "status": "inactive",
    "price_from": 0,
    "price_to": 10000,
    "quantity_from": 0,
    "quantity_to": 1000000,
    "profile_balance": 0
}
class UserPurchases(Base):
    __tablename__ = 'User_Purchases'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    user_purchases: Mapped[dict] = mapped_column(JSON, default=dict)
    def __repr__(self):
        return f"<User_Purchases(user_id={self.user_id},user_purchases={self.user_purchases})>"
class Admin(Base):
    __tablename__ = 'Admin'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stars: Mapped[float] = mapped_column(Float)
    def __repr__(self):
        return f"<Admin(stars={self.stars})>"
a_engine = create_async_engine("postgresql+asyncpg://postgres:Auth-q09786@localhost:5432/usersdb", echo=True)
Session = sessionmaker(a_engine,class_=AsyncSession,expire_on_commit=False)