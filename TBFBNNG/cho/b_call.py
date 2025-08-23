from aiogram import F,types,Router,Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
from aiogram.types import CallbackQuery,PreCheckoutQuery,InlineKeyboardMarkup,InlineKeyboardButton,LabeledPrice,Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import copy
from impo.b_st_me import bot
from impo.u_db import Session,User,Admin,ProfileSettings,default_settings,UserPurchases
from impo.b_dict import langs,keybos
from sqlalchemy import func,delete,update,select
from aiogram.methods import GetAvailableGifts
import redis.asyncio as redis
def call_router(client:redis.Redis):
    router_call = Router()
    async def prof_sett(sett):
        ul = (await client.get('lang')).decode()
        prof_sett_ch = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{langs[ul]['BSA'] if sett['status'] == 'active' else langs[ul]['BSI']}",callback_data='prof_sett_stat')],
            [InlineKeyboardButton(text=f"🎁 {langs[ul]['F']} {sett['quantity_from']:,}".replace(',', ' '),callback_data='prof_sett_qua_fr'),
             InlineKeyboardButton(text=f"🎁 {langs[ul]['F']} {sett['quantity_to']:,}".replace(',', ' '),callback_data='prof_sett_qua_to')],
            [InlineKeyboardButton(text=f"⭐ {langs[ul]['F']} {sett['price_from']:,}".replace(',', ' '),callback_data='prof_sett_pr_fr'),
             InlineKeyboardButton(text=f"⭐ {langs[ul]['F']} {sett['price_to']:,}".replace(',', ' '),callback_data='prof_sett_pr_to')],
            [InlineKeyboardButton(text=langs[ul]['PBD'], callback_data='prof_sett_dep')],
            [InlineKeyboardButton(text=langs[ul]['PD'], callback_data='prof_sett_del')],
            [InlineKeyboardButton(text=langs[ul]['BK'], callback_data='back')]
        ])
        return prof_sett_ch
    async def gift_info(targ_gift_id: str):
        gifts = await bot(GetAvailableGifts())
        for gift in gifts.gifts:
            if gift.id == targ_gift_id:
                return gift
        return None
    class Text(StatesGroup):
        quantity_from_wait = State()
        quantity_to_wait = State()
        price_from_wait = State()
        price_to_wait = State()
        balance_wait = State()
        amount_wait = State()
    @router_call.callback_query(F.data == 'au_pur')
    async def au_pur_ru(callback:types.CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        async with Session() as session:
            p = await session.scalar(select(User).where(User.user_id == u).order_by(User.user_id))
            s = p.user_profile_quantity_subtraction
            q = p.user_profile_quantity
        await callback.message.delete()
        await callback.message.answer(langs[ul]['A'].format(q=q,s=s),reply_markup=keybos[ul]['C'])
    @router_call.callback_query(F.data == 'cr_prof')
    async def cr_profi(callback:CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        async with Session() as session:
            q = await session.scalar(select(User).where(User.user_id == u))
            n = await session.scalar(select(func.max(ProfileSettings.profile_number)).where(ProfileSettings.user_id == u))
            if q.user_profile_quantity_subtraction > 0:
                if n is None:
                    n = 0
                n+=1
                new_prof = ProfileSettings(
                    user_id=u,
                    profile_number=n,
                    profile_settings={**default_settings}
                )
                q.user_profile_quantity_subtraction-=1
                session.add(new_prof)
                await session.commit()
                await callback.message.delete()
                await callback.message.answer(langs[ul]['L'], reply_markup=keybos[ul]['B'])
            else:
                await callback.message.delete()
                await callback.message.answer(langs[ul]['PE'],reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data.startswith('prof_list_'))
    async def prof_list_ru(callback:CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        index_str = callback.data.split("_")[-1]
        index_int = int(index_str)
        async with Session() as session:
            pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(index_int).limit(1))
            sett = pr.profile_settings
        await client.set(f'ind_int{u}',index_int,ex=86400)
        await callback.message.delete()
        p = await prof_sett(sett=sett)
        await callback.message.answer(langs[ul]['PI'], reply_markup=p)
    @router_call.callback_query(F.data == 'prof_sett_stat')
    async def prof_sett_bot_stat_ru(callback:CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        await client.expire(f'ind_int{u}',86400)
        ind_int = await client.get(f'ind_int{u}')
        ind_int = int(ind_int.decode())
        async with Session() as session:
            pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
            sett = copy.deepcopy(pr.profile_settings)
            sett['status'] = 'inactive' if sett['status'] == 'active' else 'active'
            pr.profile_settings = sett
            await session.commit()
            sett = pr.profile_settings
        await callback.message.delete()
        p = await prof_sett(sett=sett)
        await callback.message.answer(langs[ul]['PI'], reply_markup=p)
    @router_call.callback_query(F.data == 'prof_sett_qua_fr')
    async def prof_sett_bot_qua_fr(callback:CallbackQuery,state:FSMContext):
        ul = (await client.get('lang')).decode()
        await callback.message.delete()
        await callback.message.answer(langs[ul]['QF'])
        await state.set_state(Text.quantity_from_wait)
    @router_call.message(StateFilter(Text.quantity_from_wait))
    async def sett_qua_fr(message:Message,state:FSMContext):
        qua_f = message.text
        u = message.from_user.id
        ul = (await client.get('lang')).decode()
        try:
            qua_f = int(qua_f)
        except ValueError:
            await message.answer(langs[ul]['CSF'],reply_markup=keybos[ul]['B'])
            pass
        else:
            if qua_f >= 0:
                await state.clear()
                await client.expire(f'ind_int{u}', 86400)
                ind_int = await client.get(f'ind_int{u}')
                ind_int = int(ind_int.decode())
                async with Session() as session:
                    pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
                    sett = copy.deepcopy(pr.profile_settings)
                    sett['quantity_from'] = qua_f
                    pr.profile_settings = sett
                    await session.commit()
                    sett = pr.profile_settings
                p = await prof_sett(sett=sett)
                await message.answer(langs[ul]['PI'],reply_markup=p)
            else:
                await message.answer(langs[ul]['MSN'],reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data == 'prof_sett_qua_to')
    async def prof_sett_bot_qua_to(callback:CallbackQuery,state:FSMContext):
        ul = (await client.get('lang')).decode()
        await callback.message.delete()
        await callback.message.answer(langs[ul]['QT'])
        await state.set_state(Text.quantity_to_wait)
    @router_call.message(StateFilter(Text.quantity_to_wait))
    async def sett_qua_t(message:Message,state:FSMContext):
        qua_t = message.text
        u = message.from_user.id
        ul = (await client.get('lang')).decode()
        try:
            qua_t = int(qua_t)
        except ValueError:
            await message.answer(langs[ul]['CST'],reply_markup=keybos[ul]['B'])
            pass
        else:
            if qua_t >= 0:
                await state.clear()
                await client.expire(f'ind_int{u}', 86400)
                ind_int = await client.get(f'ind_int{u}')
                ind_int = int(ind_int.decode())
                async with Session() as session:
                    pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
                    sett = copy.deepcopy(pr.profile_settings)
                    sett['quantity_to'] = qua_t
                    pr.profile_settings = sett
                    await session.commit()
                    sett = pr.profile_settings
                p = await prof_sett(sett=sett)
                await message.answer(langs[ul]['PI'], reply_markup=p)
            else:
                await message.answer(langs[ul]['MSN'],reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data == 'prof_sett_pr_fr')
    async def prof_sett_bot_pr_fr(callback: CallbackQuery,state: FSMContext):
        ul = (await client.get('lang')).decode()
        await callback.message.delete()
        await callback.message.answer(langs[ul]['PF'])
        await state.set_state(Text.price_from_wait)
    @router_call.message(StateFilter(Text.price_from_wait))
    async def sett_pr_fr(message:Message,state:FSMContext):
        pr_f = message.text
        u = message.from_user.id
        ul = (await client.get('lang')).decode()
        try:
            pr_f = int(pr_f)
        except ValueError:
            await message.answer(langs[ul]['CPF'],reply_markup=keybos[ul]['B'])
            pass
        else:
            if pr_f >= 0:
                await state.clear()
                await client.expire(f'ind_int{u}', 86400)
                ind_int = await client.get(f'ind_int{u}')
                ind_int = int(ind_int.decode())
                async with Session() as session:
                    pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
                    sett = copy.deepcopy(pr.profile_settings)
                    sett['price_from'] = pr_f
                    pr.profile_settings = sett
                    await session.commit()
                    sett = pr.profile_settings
                p = await prof_sett(sett=sett)
                await message.answer(langs[ul]['PI'],reply_markup=p)
            else:
                await message.answer(langs[ul]['MPN'],reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data == 'prof_sett_pr_to')
    async def prof_sett_bot_pr_to(callback: CallbackQuery,state: FSMContext):
        ul = (await client.get('lang')).decode()
        await callback.message.delete()
        await callback.message.answer(langs[ul]['PT'])
        await state.set_state(Text.price_to_wait)
    @router_call.message(StateFilter(Text.price_to_wait))
    async def sett_pr_t(message:Message,state:FSMContext):
        pr_t = message.text
        u = message.from_user.id
        ul = (await client.get('lang')).decode()
        try:
            pr_t = int(pr_t)
        except ValueError:
            await message.answer(langs[ul]['CPT'],reply_markup=keybos[ul]['B'])
            pass
        else:
            if pr_t >= 0:
                await state.clear()
                await client.expire(f'ind_int{u}', 86400)
                ind_int = await client.get(f'ind_int{u}')
                ind_int = int(ind_int.decode())
                async with Session() as session:
                    pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
                    sett = copy.deepcopy(pr.profile_settings)
                    sett['price_to'] = pr_t
                    pr.profile_settings = sett
                    await session.commit()
                    sett = pr.profile_settings
                p = await prof_sett(sett=sett)
                await message.answer(langs[ul]['PI'], reply_markup=p)
            else:
                await message.answer(langs[ul]['MPN'],reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data == 'prof_sett_dep')
    async def prof_sett_bot_dep(callback:CallbackQuery,state:FSMContext):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        await client.expire(f'ind_int{u}', 86400)
        ind_int = await client.get(f'ind_int{u}')
        ind_int = int(ind_int.decode())
        async with Session() as session:
            ub = await session.scalar(select(User).where(User.user_id == u))
            b = int(ub.user_balance)
            pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
            sett = copy.deepcopy(pr.profile_settings)
            pb = sett['profile_balance']
        await callback.message.delete()
        await callback.message.answer(langs[ul]['B'].format(b=b,pb=pb))
        await state.set_state(Text.balance_wait)
    @router_call.message(StateFilter(Text.balance_wait))
    async def sett_dep(message:Message,state:FSMContext):
        bal_pr_dep = message.text
        u = message.from_user.id
        ul = (await client.get('lang')).decode()
        try:
            bal_pr_dep = int(bal_pr_dep)
        except ValueError:
            await message.answer(langs[ul]['CP'],reply_markup=keybos[ul]['B'])
            pass
        else:
            async with Session() as session:
                us_bal = await session.scalar(select(User).where(User.user_id == u))
                bal = us_bal.user_balance
                bal = int(bal)
                if bal_pr_dep < 1:
                    await message.answer(langs[ul]['MP'])
                elif bal_pr_dep > bal:
                    await message.answer(langs[ul]['NE'])
                elif bal_pr_dep <= bal:
                    await state.clear()
                    await client.expire(f'ind_int{u}', 86400)
                    ind_int = await client.get(f'ind_int{u}')
                    ind_int = int(ind_int.decode())
                    pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
                    sett = copy.deepcopy(pr.profile_settings)
                    sett['profile_balance'] += bal_pr_dep
                    pr.profile_settings = sett
                    us_bal.user_balance -= bal_pr_dep
                    await session.commit()
                    await message.answer(langs[ul]['SP'].format(b=bal_pr_dep))
    @router_call.callback_query(F.data == 'prof_sett_del')
    async def prof_sett_del(callback:CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        await client.expire(f'ind_int{u}', 86400)
        ind_int = await client.get(f'ind_int{u}')
        ind_int = int(ind_int.decode())
        async with Session() as session:
            pr = await session.scalar(select(ProfileSettings).where(ProfileSettings.user_id == u).order_by(ProfileSettings.profile_number.asc()).offset(ind_int).limit(1))
            sett = copy.deepcopy(pr.profile_settings)
            await session.execute(delete(ProfileSettings).where((ProfileSettings.user_id == u)&(ProfileSettings.profile_number == ind_int+1)))
            up = (update(User).where(User.user_id == u).values(user_profile_quantity_subtraction=User.user_profile_quantity_subtraction+1))
            bi = (update(ProfileSettings)).where((ProfileSettings.user_id == u)&(ProfileSettings.profile_number > ind_int+1)).values(profile_number=ProfileSettings.profile_number-1)
            if sett['profile_balance'] > 0:
                us_bal = await session.scalar(select(User).where(User.user_id == u))
                us_bal.user_balance+=sett['profile_balance']
                await callback.message.delete()
                await callback.message.answer(langs[ul]['PHS'].format(pr=sett['profile_balance']))
                await callback.message.answer(langs[ul]['PSD'], reply_markup=keybos[ul]['B'])
            else:
                await callback.message.delete()
                await callback.message.answer(langs[ul]['PSD'],reply_markup=keybos[ul]['B'])
            await session.execute(up)
            await session.execute(bi)
            await session.commit()
    @router_call.callback_query(F.data == 'prof_sett_ba')
    async def lang_ba_ru(callback:types.CallbackQuery,state:FSMContext):
        u = callback.from_user.id
        await client.delete(f'ind_int{u}')
        await state.clear()
        ul = (await client.get('lang')).decode()
        us = callback.from_user.username
        await callback.message.delete()
        await callback.message.answer(langs[ul]['H'].format(us=us),reply_markup=keybos[ul]['M'])
    @router_call.callback_query(F.data == 'dep_t_a')
    async def dep_t_a(callback:CallbackQuery,state:FSMContext):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        async with Session() as session:
            ba = await session.scalar(select(User).where(User.user_id == u))
            b = int(ba.user_balance)
        await callback.message.delete()
        await callback.message.answer(langs[ul]['D'].format(b=b),reply_markup=keybos[ul]['B'])
        await state.set_state(Text.amount_wait)
    @router_call.message(StateFilter(Text.amount_wait))
    async def dep(message:Message,state:FSMContext):
        ge_am = message.text
        ul = (await client.get('lang')).decode()
        try:
            ge_am = int(ge_am)
        except ValueError:
            await message.answer(langs[ul]['CS'],reply_markup=keybos[ul]['B'])
            pass
        else:
            if ge_am >= 50:
                await state.clear()
                await client.set('pur',ge_am)
                prices = [LabeledPrice(label='XTR',amount=ge_am)]
                builder = InlineKeyboardBuilder()
                builder.button(text=langs[ul]['CD'], pay=True)
                builder.adjust(1)
                await message.answer_invoice(
                    title = langs[ul]['DT'],
                    description = langs[ul]['DI'].format(ge_am=ge_am),
                    prices=prices,
                    provider_token='',
                    payload=str(ge_am),
                    currency='XTR',
                    reply_markup=builder.as_markup(),
                    )
            else:
                await message.answer(langs[ul]['MS'])
    @router_call.pre_checkout_query()
    async def check_pay_ru(pre_checkout_query:PreCheckoutQuery,bot:Bot):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    @router_call.message(F.successful_payment)
    async def succes_pay_ru(message:Message):
        u = message.from_user.id
        ul = (await client.get('lang')).decode()
        us = await client.get('pur')
        us = int(us.decode())
        await client.delete('pur')
        af = (2/100)*us
        user_res_amo = us-af
        async with Session() as session:
            use = await session.scalar(select(User).filter(User.user_id == u))
            use.user_balance += user_res_amo
            use.user_balance_max += user_res_amo
            ub = use.user_balance
            await message.answer(langs[ul]['YB'].format(ub=ub),reply_markup=keybos[ul]['B'])
            admin = await session.scalar(select(Admin))
            admin.stars += af
            await session.commit()
    @router_call.callback_query(F.data.startswith('us_pur_'))
    async def us_pur(callback:types.CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        index_str = callback.data.split("_")[-1]
        index_int = int(index_str)
        async with Session() as session:
            fi_u_pu = await session.scalar(select(UserPurchases).where(UserPurchases.user_id == u).order_by(UserPurchases.user_purchases_number.asc()).offset(index_int).limit(1))
            use_pur = fi_u_pu.user_purchases
        gi_anim = await gift_info(use_pur['gift_id'])
        await callback.message.delete()
        await callback.message.answer(langs[ul]['BGI'].format(stick=gi_anim.sticker.emoji,pr=gi_anim.star_count,time=use_pur['gift_time']),reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data == 'ref_sys')
    async def ref_sys_ru(callback:types.CallbackQuery):
        u = callback.from_user.id
        ul = (await client.get('lang')).decode()
        async with Session() as session:
            us = await session.scalar(select(User).where(User.user_id == u))
            r = us.user_id
            rs = us.user_referral
        await callback.message.delete()
        await callback.message.answer(langs[ul]['R'].format(r=r,rs=rs),reply_markup=keybos[ul]['B'])
    @router_call.callback_query(F.data == 'ch_lang')
    async def ch_lang_ru(callback:types.CallbackQuery):
        ul = (await client.get('lang')).decode()
        await callback.message.delete()
        await callback.message.answer(langs[ul]['C'],reply_markup=keybos[ul]['L'])
    @router_call.callback_query(F.data == 'ch_t_ru')
    async def ch_fr_ru_t_en(callback:types.CallbackQuery):
        u = callback.from_user.id
        async with Session() as session:
            us = await session.scalar(select(User).where(User.user_id == u))
            us.user_lang = 'ru'
            await session.commit()
        await client.set('lang','ru')
        await callback.message.delete()
        await callback.message.answer(langs['ru']['CH'],reply_markup=keybos['ru']['B'])
    @router_call.callback_query(F.data == 'ch_t_en')
    async def ch_fr_ru_t_en(callback:types.CallbackQuery):
        u = callback.from_user.id
        async with Session() as session:
            us = await session.scalar(select(User).where(User.user_id == u))
            us.user_lang = 'en'
            await session.commit()
        await client.set('lang','en')
        await callback.message.delete()
        await callback.message.answer(langs['en']['CH'],reply_markup=keybos['en']['B'])
    @router_call.callback_query(F.data == 'ch_t_uk')
    async def ch_fr_ru_t_uk(callback:types.CallbackQuery):
        u = callback.from_user.id
        async with Session() as session:
            us = await session.scalar(select(User).where(User.user_id == u))
            us.user_lang = 'uk'
            await session.commit()
        await client.set('lang','uk')
        await callback.message.delete()
        await callback.message.answer(langs['uk']['CH'],reply_markup=keybos['uk']['B'])
    @router_call.callback_query(F.data == 'back')
    async def lang_ba_ru(callback:types.CallbackQuery,state:FSMContext):
        ul = (await client.get('lang')).decode()
        await client.delete('rig')
        us = callback.from_user.username
        await callback.message.delete()
        await state.clear()
        await callback.message.answer(langs[ul]['H'].format(us=us),reply_markup=keybos[ul]['M'])
    return router_call