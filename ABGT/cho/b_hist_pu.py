from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery
from aiogram import Router,F
from impo.u_db import Session,UserPurchases
from impo.b_dict import langs,keybos
import locale
from datetime import datetime
from zoneinfo import ZoneInfo
import redis.asyncio as redis
from sqlalchemy import select,cast,String
def hist_pu_router(client:redis.Redis):
    router_hist_pu = Router()
    @router_hist_pu.callback_query(F.data == 'hist_pu_rig')
    async def hist_pu_rig(callback:CallbackQuery):
        u=callback.from_user.id
        ul=(await client.get('lang')).decode()
        ch_red=await client.expire('rig',86400)
        if ch_red is True:
            rign=int((await client.get('rig')).decode())
            r=rign*5
            async with Session() as session:
                us_pur=await session.scalars(select(UserPurchases).where(UserPurchases.user_id==u).order_by(UserPurchases.user_purchases_number.asc()).offset(r).limit(6))
                us_pur_dec=us_pur.all()
                ne=None
                if len(us_pur_dec)==6:
                    us_pur_dec=us_pur_dec[:-1]
                    ne=True
                if ul=='ru':
                    locale.setlocale(locale.LC_TIME,"ru_RU.UTF-8")
                elif ul=='en':
                    locale.setlocale(locale.LC_TIME,"en_US.UTF-8")
                butt_li=[]
                await callback.message.delete()
                for i in range(len(us_pur_dec)):
                    gift_time=us_pur_dec[i].user_purchases['gift_time']
                    nee_id=await session.scalar(select(UserPurchases.user_purchases_number).where(UserPurchases.user_id==u,cast(UserPurchases.user_purchases['gift_time'],String)==f'"{gift_time}"'))
                    gift_time=datetime.strptime(gift_time,"%Y.%m.%d | %H:%M:%S")
                    gift_time=gift_time.replace(tzinfo=ZoneInfo("Europe/Kyiv"))
                    if ul=='ru':
                        gift_time=gift_time.astimezone(ZoneInfo("Europe/Moscow"))
                        gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                        gift_time=f'🇷🇺 UTC+3: {gift_time}'
                    elif ul=='en':
                        gift_time=gift_time.astimezone(ZoneInfo("America/New_York"))
                        gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                        gift_time=f'🇺🇸 UTC+4: {gift_time}'
                    else:
                        gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                        gift_time=f'🇺🇦 UTC+3: {gift_time}'
                    butt_li.append([InlineKeyboardButton(text=f"🎁{gift_time}🎁",callback_data=f'us_pur_{nee_id-1}')])
                if ne:
                    butt_li.append([InlineKeyboardButton(text='⬅️',callback_data='hist_pu_left'),InlineKeyboardButton(text='➡️',callback_data='hist_pu_rig')])
                else:
                    butt_li.append([InlineKeyboardButton(text='⬅️',callback_data='hist_pu_left')])
                rign+=1
                await client.set('rig',rign,ex=86400)
        else:
            async with Session() as session:
                us_prof=await session.scalar(select(UserPurchases).where(UserPurchases.user_id == u))
                if not us_prof:
                    await callback.message.delete()
                    await callback.message.answer(langs[ul]['HNP'],reply_markup=keybos[ul]['B'])
                else:
                    us_pur=await session.scalars(select(UserPurchases).where(UserPurchases.user_id==u).order_by(UserPurchases.user_purchases_number.asc()).limit(6))
                    us_pur_dec=us_pur.all()
                    if len(us_pur_dec)==6:
                        us_pur_dec=us_pur_dec[:-1]
                        ne=True
                    if ul=='ru':
                        locale.setlocale(locale.LC_TIME,"ru_RU.UTF-8")
                    elif ul=='en':
                        locale.setlocale(locale.LC_TIME,"en_US.UTF-8")
                    butt_li=[]
                    await callback.message.delete()
                    for i in range(len(us_pur_dec)):
                        gift_time=us_pur_dec[i].user_purchases['gift_time']
                        gift_time=datetime.strptime(gift_time,"%Y.%m.%d | %H:%M:%S")
                        gift_time=gift_time.replace(tzinfo=ZoneInfo("Europe/Kyiv"))
                        if ul=='ru':
                            gift_time=gift_time.astimezone(ZoneInfo("Europe/Moscow"))
                            gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                            gift_time=f'🇷🇺 UTC+3: {gift_time}'
                        elif ul=='en':
                            gift_time=gift_time.astimezone(ZoneInfo("America/New_York"))
                            gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                            gift_time=f'🇺🇸 UTC+4: {gift_time}'
                        else:
                            gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                            gift_time=f'🇺🇦 UTC+3: {gift_time}'
                        butt_li.append([InlineKeyboardButton(text=f"🎁{gift_time}🎁",callback_data=f'us_pur_{i}')])
                    if ne:
                        butt_li.append([InlineKeyboardButton(text='➡️',callback_data='hist_pu_rig')])
                        await client.set('rig', 1, ex=86400)
        butt_li.append([InlineKeyboardButton(text=langs[ul]['BK'],callback_data='back')])
        us_pur_list=InlineKeyboardMarkup(inline_keyboard=butt_li)
        await callback.message.answer(langs[ul]['YG'],reply_markup=us_pur_list)
    @router_hist_pu.callback_query(F.data == 'hist_pu_left')
    async def hist_pu_left(callback:CallbackQuery):
        u=callback.from_user.id
        ul=(await client.get('lang')).decode()
        await client.expire('rig',86400)
        rign=int((await client.get('rig')).decode())
        rign-=1
        await client.set('rig', rign, ex=86400)
        async with Session() as session:
            r=rign*5-5
            us_pur=await session.scalars(select(UserPurchases).where(UserPurchases.user_id==u).order_by(UserPurchases.user_purchases_number.asc()).offset(r).limit(6))
            us_pur_dec=us_pur.all()
            ne=None
            if len(us_pur_dec)==6:
                us_pur_dec=us_pur_dec[:-1]
                ne=True
            if ul=='ru':
                locale.setlocale(locale.LC_TIME,"ru_RU.UTF-8")
            elif ul=='en':
                locale.setlocale(locale.LC_TIME,"en_US.UTF-8")
            butt_li=[]
            await callback.message.delete()
            for i in range(len(us_pur_dec)):
                gift_time=us_pur_dec[i].user_purchases['gift_time']
                nee_id=await session.scalar(select(UserPurchases.user_purchases_number).where(UserPurchases.user_id==u,cast(UserPurchases.user_purchases['gift_time'],String)==f'"{gift_time}"'))
                gift_time=datetime.strptime(gift_time,"%Y.%m.%d | %H:%M:%S")
                gift_time=gift_time.replace(tzinfo=ZoneInfo("Europe/Kyiv"))
                if ul=='ru':
                    gift_time=gift_time.astimezone(ZoneInfo("Europe/Moscow"))
                    gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                    gift_time=f'🇷🇺 UTC+3: {gift_time}'
                elif ul=='en':
                    gift_time=gift_time.astimezone(ZoneInfo("America/New_York"))
                    gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                    gift_time=f'🇺🇸 UTC+4: {gift_time}'
                else:
                    gift_time=gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                    gift_time=f'🇺🇦 UTC+3: {gift_time}'
                butt_li.append([InlineKeyboardButton(text=f"🎁{gift_time}🎁",callback_data=f'us_pur_{nee_id-1}')])
            if ne:
                ch_p=await session.scalar(select(UserPurchases).where(UserPurchases.user_id==u))
                if ch_p.user_purchases==us_pur_dec[0].user_purchases:
                    butt_li.append([InlineKeyboardButton(text='➡️',callback_data='hist_pu_rig')])
                else:
                    butt_li.append([InlineKeyboardButton(text='⬅️',callback_data='hist_pu_left'),InlineKeyboardButton(text='➡️',callback_data='hist_pu_rig')])
            else:
                butt_li.append([InlineKeyboardButton(text='⬅️',callback_data='hist_pu_left')])
            butt_li.append([InlineKeyboardButton(text=langs[ul]['BK'],callback_data='back')])
            us_pur_list = InlineKeyboardMarkup(inline_keyboard=butt_li)
            await callback.message.answer(langs[ul]['YG'], reply_markup=us_pur_list)
    return router_hist_pu
