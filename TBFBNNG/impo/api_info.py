from fastapi import FastAPI,HTTPException
from typing import List,Optional
from impo.u_db import User,UserPurchases,ProfileSettings,Admin,Session
from sqlalchemy import select
from pydantic import BaseModel,ConfigDict
class UsAll(BaseModel):
    id:int
    user_id:int
    user_username:str
    user_lang:str
    user_balance:float
    user_balance_max:float
    user_referral:int
    user_profile_quantity:int
    model_config = ConfigDict(from_attributes=True)
class JsonPur(BaseModel):
    gift_id:str
    gift_time:str
class PurAll(BaseModel):
    id:int
    user_id:int
    user_purchases_number:int
    user_purchases:JsonPur
    model_config = ConfigDict(from_attributes=True)
class JsonPro(BaseModel):
    status:str
    price_from:int
    price_to:int
    quantity_from:int
    quantity_to:int
    profile_balance:int
class ProAll(BaseModel):
    id:int
    user_id:int
    profile_number:int
    profile_settings:JsonPro
    model_config = ConfigDict(from_attributes=True)
class Adm(BaseModel):
    id:int
    stars:float
class ForSear(BaseModel):
    id:Optional[int] = None
    user_id:Optional[int] = None
    user_username:Optional[str] = None
    user_lang:Optional[str] = None
    user_balance:Optional[float] = None
    user_balance_max:Optional[float] = None
    user_referral:Optional[int] = None
    user_profile_quantity:Optional[int] = None
    profile_number:Optional[int] = None
    profile_settings:Optional[JsonPro] = None
    user_purchases_number:Optional[int] = None
    user_purchases:Optional[JsonPur] = None
    model_config = ConfigDict(from_attributes=True)
ai = FastAPI(title='FastAPI for TBFBNNG',description='Flexible API for working with database')
@ai.get('/',summary='Initial message')
async def s() -> None:
    return None
@ai.get('/allus',response_model=List[UsAll],summary='Info about AllUser',description='Returns all information from table User')
async def all_use():
    async with Session() as session:
        all_us = await session.execute(select(User))
        all_us = all_us.scalars().all()
        return all_us
@ai.get('/allpr',response_model=List[ProAll],summary='Info about AllProfileSettings',description='Returns all information from table ProfileSettings')
async def all_pro():
    async with Session() as session:
        all_prof = await session.execute(select(ProfileSettings))
        all_prof = all_prof.scalars().all()
        return all_prof
@ai.get('/allpur',response_model=List[PurAll],summary='Info about AllUserPurchases',description='Returns all information from table UserPurchases')
async def all_purc():
    async with Session() as session:
        all_pur = await session.execute(select(UserPurchases))
        all_pur = all_pur.scalars().all()
        return all_pur
@ai.get('/adm',response_model=List[Adm],summary='Info about Admin',description='Returns all information from table Admin')
async def adm():
    async with Session() as session:
        admi = await session.scalars(select(Admin))
        return admi
@ai.get('/search/{wh_sea}/{us_id}',response_model=List[ForSear],summary='Info about User',description='Returns information about any user from any table')
async def search(wh_sea: str,us_id: int):
    async with Session() as session:
        if wh_sea == 'users':
            sea = await session.scalars(select(User).where(User.user_id==us_id))
            sea = sea.all()
        elif wh_sea == 'profiles':
            sea = await session.scalars(select(ProfileSettings).where(ProfileSettings.user_id==us_id))
            sea = sea.all()
        elif wh_sea == 'purchases':
            sea = await session.scalars(select(UserPurchases).where(UserPurchases.user_id==us_id))
            sea = sea.all()
        else:
            raise HTTPException(status_code=400,detail='Invalid search query.')
    if not sea:
        if wh_sea == 'users':
            det = 'User'
        elif wh_sea == 'profiles':
            det = 'ProfileSettings'
        else:
            det = 'UserPurchases'
        raise HTTPException(status_code=400,detail=f'The user with this ID has no records in the Table {det}.')
    return sea
@ai.get('/about/{us_id}',summary='All information about the user',description='Returns all information about the user')
async def about(us_id:int):
    async with Session() as session:
        abou_1 = await session.scalars(select(User).where(User.user_id==us_id))
        abou_1 = abou_1.all()
        abou_2 = await session.scalars(select(ProfileSettings).where(ProfileSettings.user_id==us_id))
        abou_2 = abou_2.all()
        abou_3 = await session.scalars(select(UserPurchases).where(UserPurchases.user_id==us_id))
        abou_3 = abou_3.all()
        return abou_1,abou_2,abou_3
