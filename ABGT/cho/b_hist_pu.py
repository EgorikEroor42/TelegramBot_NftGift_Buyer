from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram import Router,F
from aiogram.types import CallbackQuery
from impo.u_db import Session,UserPurchases
from impo.b_dict import langs,keybos
from sqlalchemy import select
import locale
from datetime import datetime
from zoneinfo import ZoneInfo
import redis.asyncio as redis
def hist_pu_router(client:redis.Redis):
    router_hist_pu = Router()
    @router_hist_pu.callback_query(F.data == 'pur_h')
    async def pur_h(callback:CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        async with Session() as session:
            us_prof = await session.scalar(select(UserPurchases).where(UserPurchases.user_id == u))
            if not us_prof:
                await callback.message.delete()
                await callback.message.answer(langs[ul]['HNP'],reply_markup=keybos[ul]['B'])
            else:
                us_pur = await session.scalars(select(UserPurchases.user_purchases).where(UserPurchases.user_id == u))
                us_pur_all = us_pur.all()
                if ul == 'ru':
                    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
                elif ul == 'en':
                    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
                butt_li = []
                for i,pur in enumerate(us_pur_all):
                    gift_time = pur[f'gift_time{i}']
                    gift_time = datetime.strptime(gift_time, "%Y.%m.%d | %H:%M:%S")
                    gift_time = gift_time.replace(tzinfo=ZoneInfo("Europe/Kyiv"))
                    if ul == 'ru':
                        gift_time = gift_time.astimezone(ZoneInfo("Europe/Moscow"))
                        gift_time = gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                        gift_time = f'🇷🇺 UTC+3: {gift_time}'
                    elif ul == 'en':
                        gift_time = gift_time.astimezone(ZoneInfo("America/New_York"))
                        gift_time = gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                        gift_time = f'🇺🇸 UTC+4: {gift_time}'
                    else:
                        gift_time = gift_time.strftime("%Y.%m.%d | %H:%M:%S")
                        gift_time = f'🇺🇦 UTC+3: {gift_time}'
                    butt_li.append([
                        InlineKeyboardButton(
                            text=f"🎁{gift_time}🎁",callback_data=f'us_pur_{i}'
                        )
                    ])
                butt_li.append([
                    InlineKeyboardButton(
                        text='🔙 Назад', callback_data='back'
                    )
                ])
                us_pur_list = InlineKeyboardMarkup(inline_keyboard=butt_li)
                await callback.message.answer(langs[ul]['YG'],reply_markup=us_pur_list)
    return router_hist_pu