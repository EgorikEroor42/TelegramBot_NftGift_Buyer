from zoneinfo import ZoneInfo
from aiogram.types.gifts import Gifts,Gift
from impo.b_st_me import bot
from aiogram.methods import SendGift
from impo.u_db import User,Session,ProfileSettings,UserPurchases
import asyncio
from datetime import datetime
from sqlalchemy import select
import copy
async def check_gift_list():
    wait_gifts_list = None
    while True:
        while True:
            result: Gifts = await bot.get_available_gifts()
            gifts: list[Gift] = result.gifts
            gift_ids = [int(gift.id) for gift in gifts]
            if wait_gifts_list is None:
                wait_gifts_list = gift_ids
            ua_time = datetime.now(ZoneInfo("Europe/Kyiv"))
            time = ua_time.hour
            if time in [13, 23]:
                await asyncio.sleep(0.1)
            elif time in [13, 14, 15, 21, 22, 23]:
                await asyncio.sleep(1)
            elif time in [16, 17, 18, 19, 20]:
                await asyncio.sleep(3)
            else:
                await asyncio.sleep(5)
            if set(wait_gifts_list) != set(gift_ids):
                break
        async with Session() as session:
            users_is_deposit_balance = (await session.scalars(select(User.user_id).where(User.user_balance_max > 0).order_by(User.user_id.desc()))).all()
            users_balance_max = (await session.execute(select(User.user_id, User.user_balance_max).where(User.user_id.in_(users_is_deposit_balance)).order_by(User.user_balance_max.desc()))).all()
            for i in range(len(users_balance_max)):
                user_profile_quantity = (await session.scalars(select(ProfileSettings.profile_settings).where(ProfileSettings.user_id == users_balance_max[i][0]))).all()
                if user_profile_quantity:
                    for j,k in enumerate(user_profile_quantity):
                        result: Gifts = await bot.get_available_gifts()
                        gifts: list[Gift] = result.gifts
                        gift_ids = [int(gift.id) for gift in gifts]
                        new_gift_ids = list(set(gift_ids) - set(wait_gifts_list))
                        wait_gifts_list = gift_ids
                        new_gifts = {
                            int(gift.id): {
                                'price': int(gift.star_count),
                                'quantity': int(gift.remaining_count)
                            }
                            for gift in gifts if int(gift.id) in new_gift_ids
                        }
                        for get_gift_id, get_gift_info in new_gifts.items():
                            if k['quantity_from'] <= get_gift_info['quantity'] <= k['quantity_to'] and k['price_from'] <= get_gift_info['price'] <= k['price_to'] and k['profile_balance'] >= get_gift_info['price']:
                                repeat_purchases = int(k['profile_balance']/get_gift_info['price'])
                                pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == users_balance_max[i][0]).order_by(ProfileSettings.profile_number.asc()).offset(j).limit(1))
                                sett = copy.deepcopy(pr.profile_settings)
                                sett['profile_balance']-=repeat_purchases*get_gift_info['price']
                                pr.profile_settings = sett
                                await session.commit()
                                for l in range(repeat_purchases):
                                    get_gift_id = str(get_gift_id)
                                    await bot(SendGift(gift_id=get_gift_id,user_id=users_balance_max[i]))
                                    ua_time = datetime.now(ZoneInfo("Europe/Kyiv"))
                                    gift_time = ua_time.strftime("%Y.%m.%d | %H:%M:%S")
                                    new_gift = UserPurchases(
                                        user_id=users_balance_max[i],
                                        user_purchases={
                                            'gift_id': get_gift_id,
                                            'gift_time': gift_time
                                        }
                                    )
                                    session.add(new_gift)
                                    await asyncio.sleep(0.1)
            while True:
                result: Gifts = await bot.get_available_gifts()
                gifts: list[Gift] = result.gifts
                gift_ids = [int(gift.id) for gift in gifts]
                if set(wait_gifts_list) == set(gift_ids):
                    break
                ua_time = datetime.now(ZoneInfo("Europe/Kyiv"))
                time = ua_time.hour
                if time in [13, 23]:
                    await asyncio.sleep(0.1)
                elif time in [13, 14, 15, 21, 22, 23]:
                    await asyncio.sleep(1)
                elif time in [16, 17, 18, 19, 20]:
                    await asyncio.sleep(3)
                else:
                    await asyncio.sleep(5)