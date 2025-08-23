from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram import Router,F
from aiogram.types import CallbackQuery
from impo.u_db import Session,ProfileSettings
from impo.b_dict import langs,keybos
from sqlalchemy import select
import redis.asyncio as redis
def list_prof_router(client:redis.Redis):
    router_list_prof = Router()
    @router_list_prof.callback_query(F.data == 'list_prof')
    async def list_prof(callback:CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        async with Session() as session:
            us_prof_num = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u))
            if not us_prof_num:
                await callback.message.delete()
                await callback.message.answer(langs[ul]['NPA'],reply_markup=keybos[ul]['B'])
            else:
                prof_num = await session.scalars(select(ProfileSettings.profile_settings).where(ProfileSettings.user_id == u))
                print(prof_num)
                prof_num_a_set = prof_num.all()
                butt_li = []
                for i in range(len(prof_num_a_set)):
                    stat = '🟢' if prof_num_a_set[i]['status'] == 'active' else '🔴'
                    qf = "{:,}".format(prof_num_a_set[i]['quantity_from']).replace(',', ' ')
                    qt = "{:,}".format(prof_num_a_set[i]['quantity_to']).replace(',', ' ')
                    pr_f = "{:,}".format(prof_num_a_set[i]['price_from']).replace(',', ' ')
                    pr_t = "{:,}".format(prof_num_a_set[i]['price_to']).replace(',', ' ')
                    butt_li.append([
                        InlineKeyboardButton(
                            text=f"{stat} | 🎁{qf} - {qt} | ⭐️{pr_f} - {pr_t}",callback_data=f'prof_list_{i}'
                        )
                    ])
                butt_li.append([
                    InlineKeyboardButton(
                        text='🔙 Назад', callback_data='back'
                    )
                ])
                prof_list_ru = InlineKeyboardMarkup(inline_keyboard=butt_li)
                await callback.message.delete()
                await callback.message.answer(langs[ul]['YL'],reply_markup=prof_list_ru)
    return router_list_prof