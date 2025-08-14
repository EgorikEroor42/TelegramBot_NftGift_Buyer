import asyncio
from u_db import Base,s_engine,a_engine,Admin,Session
from sqlalchemy import select
from impo.b_st_me import start_router,bot
from cho.b_call import call_router
from cho.b_list_prof import list_prof_router
from impo.b_g import check_gift_list
from cho.b_hist_pu import hist_pu_router
from aiogram import Dispatcher
import redis.asyncio as redis
async def admin_fee():
    async with Session() as session:
        adm = await session.scalar(select(Admin))
        if adm is None:
            new_adm = Admin(stars=0)
            session.add(new_adm)
            await session.commit()
async def main():
    Base.metadata.create_all(s_engine)
    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    dp = Dispatcher()
    asyncio.create_task(check_gift_list())
    asyncio.create_task(admin_fee())
    client = redis.Redis(host='localhost', port=Your_port, db=Your_name_redis_base)
    dp.include_router(start_router(client))
    dp.include_router(call_router(client))
    dp.include_router(hist_pu_router(client))
    dp.include_router(list_prof_router(client))
    await dp.start_polling(bot)
if __name__ == "__main__":

    asyncio.run(main())
