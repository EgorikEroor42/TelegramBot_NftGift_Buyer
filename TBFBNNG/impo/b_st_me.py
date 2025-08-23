from aiogram import Router,types,Bot,Dispatcher
from aiogram.filters import CommandStart,CommandObject
from aiogram.fsm.context import FSMContext
from impo.u_db import User,Session
from sqlalchemy import select
from impo.b_dict import langs,keybos
import redis.asyncio as redis
bot = Bot('8384746324:AAH8oE1zThi7VFwc9A_z3S6r9w75dlM3po4')
dp = Dispatcher()
def start_router(client:redis.Redis):
    router_start = Router()
    @router_start.message(CommandStart(deep_link=True))
    async def check_ref(message:types.Message,command:CommandObject):
        ref = command.args
        await client.set('ref',ref,ex=86400)
    @router_start.message(CommandStart())
    async def start(message:types.Message,state:FSMContext):
        u = message.from_user.id
        us = message.from_user.username
        ul = message.from_user.language_code
        async with Session() as session:
            cus = await session.scalar(select(User).where(User.user_id==u))
            if not cus:
                if us is None:
                    us = 'Guest'
                if ul not in ['ru', 'en', 'uk']:
                    ul = 'en'
                new_user = User(user_id=u,user_username=us,user_lang=ul)
                session.add(new_user)
                await session.commit()
                await client.set('lang',ul)
                usi = await client.get('ref')
                if usi is not None:
                    usi = int(usi.decode())
                    invus = await session.scalar(select(User).where(User.user_id == usi))
                    if invus:
                        invus.user_referral += 1
                        await session.commit()
                        await client.delete('ref')
                        check_ref_prog = invus.user_referral
                        if check_ref_prog % 3 == 0:
                            invus.user_profile_quantity+=1
                            invus.user_profile_quantity_subtraction+=1
                            await session.commit()
                    else:
                        await message.answer(langs[ul]['UNF'])
            await message.answer(langs[ul]['H'].format(us=us),reply_markup=keybos[ul]['M'])
            await state.clear()
            await client.delete('rig')
    return router_start