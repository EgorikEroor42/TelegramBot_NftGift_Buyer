from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
ru_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚡ Автопокупка',callback_data='au_pur'),
     InlineKeyboardButton(text='🌟 Пополнение баланса',callback_data='dep_t_a')],
    [InlineKeyboardButton(text='⚖ История покупок',callback_data='hist_pu_rig'),
     InlineKeyboardButton(text='👤 Реферальная программа',callback_data='ref_sys')],
    [InlineKeyboardButton(text='🇷🇺 Сменить язык',callback_data='ch_lang')]
])
en_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚡ Auto purchase',callback_data='au_pur'),
     InlineKeyboardButton(text='🌟 Deposit',callback_data='dep_t_a')],
    [InlineKeyboardButton(text='⚖ Your purchase history',callback_data='hist_pu_rig'),
     InlineKeyboardButton(text='👤 Referral program',callback_data='ref_sys')],
    [InlineKeyboardButton(text='🇺🇸 Change language',callback_data='ch_lang')]
])
uk_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚡ Автокупівля',callback_data='au_pur'),
     InlineKeyboardButton(text='🌟 Поповнення рахунку',callback_data='dep_t_a')],
    [InlineKeyboardButton(text='⚖ Історія ваших придбань',callback_data='hist_pu_rig'),
     InlineKeyboardButton(text='👤 Реферальна система',callback_data='ref_sys')],
    [InlineKeyboardButton(text='🇺🇦 Змінити мову',callback_data='ch_lang')]
])
cr_prof_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙ Создать профиль',callback_data='cr_prof')],
    [InlineKeyboardButton(text='📃 Список профилей', callback_data='list_prof')],
    [InlineKeyboardButton(text='🔙 Назад',callback_data='back')]
])
cr_prof_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙ Create Profile', callback_data='cr_prof')],
    [InlineKeyboardButton(text='📃 Profile List', callback_data='list_prof')],
    [InlineKeyboardButton(text='🔙 Back', callback_data='back')]
])
cr_prof_uk = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙ Створити профіль', callback_data='cr_prof')],
    [InlineKeyboardButton(text='📃 Список профілів', callback_data='list_prof')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
])
ru_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='back')]
])
en_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Back',callback_data='back')]
])
uk_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад ',callback_data='back')]
])
ru_lang = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇺🇦',callback_data='ch_t_uk'),
     InlineKeyboardButton(text='🇺🇸',callback_data='ch_t_en')],
    [InlineKeyboardButton(text='🔙 Назад',callback_data='back')]
])
en_lang = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇺🇦',callback_data='ch_t_uk'),
     InlineKeyboardButton(text='🇷🇺',callback_data='ch_t_ru')],
    [InlineKeyboardButton(text='🔙 Back',callback_data='back')]
])
uk_lang = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇷🇺',callback_data='ch_t_ru'),
     InlineKeyboardButton(text='🇺🇸',callback_data='ch_t_en')],
    [InlineKeyboardButton(text='🔙 Назад',callback_data='back')]
])
langs = {
    'ru': {
        'H': 'Здравствуйте, {us}.\nЭтот бот автоматически скупает свежие NFT-подарки в Telegram. Основной функционал:',
        'A': '⚡ Автопокупка активируется сразу после релиза новых NFT-подарков.\nИзначально можно создать до {q} профилей.\nОставшееся количество профилей: {s}.',
        'D': '🌟 Баланс: {b} звёзд.\nПополнение осуществляется в звёздах.\nКомиссия: 2%.\nМинимальное пополнение: 50 звёзд.\nУкажите количество для пополнения:',
        'P': '⚖ История ваших покупок:',
        'R': '👤 За каждые 3 приглашённых пользователя предоставляется 1 дополнительный профиль.\nПриглашено: {rs} пользователей.\nВаша реферальная ссылка:\nhttps://t.me/FastGiftBuyerBot?start={r}',
        'C': '🇷🇺 Выберите язык для интерфейса:',
        'CH': '🇷🇺 Вы сменили язык на русский.',
        'L': '📃 Откройте список профилей, чтобы выполнить настройку профиля.',
        'QF': 'Введите, от какого количества копий вы хотите начинать скупать NFT-подарки:',
        'QT': 'Введите, до какого количества копий вы хотите скупать NFT-подарки:',
        'PF': 'Укажите цену, от которой начать скупку NFT-подарков:',
        'PT': 'Укажите цену, до которой скупать NFT-подарков:',
        'B': 'На вашем балансе: {b} звёзд.\nНа балансе профиля: {pb}\nВведите сумму, на которую хотите пополнить баланс профиля:',
        'PSD': '✅ Профиль успешно удалён.',
        'CP': '🚫 Введите корректное число для пополнения баланса профиля.',
        'MP': '🚫 Минимально допустимая сумма пополнения баланса профиля - 1 звезда.',
        'NE': '🚫 Недостаточно звёзд на балансе для выполнения операции.',
        'SP': '👌 Баланс профиля успешно пополнен на {b} звёзд.',
        'CPF': '🚫 Введите корректное число, от какой цены вы хотите начать скупать NFT-подарки.',
        'PI': '🎁 Количество: укажите диапазон — от какого до какого количества копий свежих NFT-подарков скупать.\n⭐️ Цена: укажите диапазон — от какой до какой цены скупать свежие NFT-подарки.',
        'MPN': '🚫 Минимальная допустимая цена для скупки NFT-подарков - 0.',
        'CPT': '🚫 Введите корректное число, до какой цены вы хотите скупать NFT-подарки.',
        'CST': '🚫 Введите корректное число, до какого количества копий вы хотите скупать NFT-подарки.',
        'MSN': '🚫 Минимальное допустимое число копий для скупки NFT-подарков: 0.',
        'CSF': '🚫 Введите корректное число, от какого количества копий вы хотите начинать скупать NFT-подарки.',
        'CS': '🚫 Введите корректное количество звёзд.',
        'CD': '⭐ Пополнить',
        'DT': 'Пополнения баланса.',
        'DI': '⭐ Пополнение баланса на {ge_am} звёзд.',
        'MS': '🚫 Минимальное количество звёзд для пополнения: 50.',
        'PE': '🥹 Профили закончились.',
        'YB': 'На вашем балансе: {ub}',
        'YL': '📃 Ваш список профилей:',
        'BSA': '🟢 Бот включён',
        'BSI': '🔴 Бот выключен',
        'F': 'От:',
        'T': 'До:',
        'PBD': '⭐ Пополнить баланс профиля',
        'PD': '🚫 Удалить профиль',
        'BK': '🔙 Назад',
        'UNF': '🤔 Пользователь, пригласивший вас, не существует.',
        'NPA': '😡 Профили отсутствуют. Создайте хотя бы один, чтобы продолжить.',
        'YG': '🎁 Ваш список покупок:',
        'HNP': '😭 У вас отсутствуют какие-либо покупки.',
        'BGI': '🎁НФТ-подарок: {stick}\n🌟Цена: {pr} звёзд.\n🕘Дата покупки: {time}',
        'PHS': '⚠️ В данном профиле находилось {pr} звёзд.\nУказанная сумма была возвращена на баланс.'
},
    'en': {
        'H': 'Hello, {us}.\nThis bot automatically buys fresh NFT gifts on Telegram. Main features:',
        'A': '⚡ Auto-purchase is activated immediately after the release of new NFT gifts.\nInitially, you can create up to {q} profiles.\nRemaining profiles: {s}.',
        'D': '🌟 Balance: {b} stars.\nTop-up is made in stars.\nFee: 2%.\nMinimum top-up: 50 stars.\nEnter the amount to top up:',
        'P': '⚖ Your purchase history:',
        'R': '👤 For every 3 invited users, you get 1 additional profile.\nInvited: {rs} users.\nYour referral link:\nhttps://t.me/FastGiftBuyerBot?start={r}',
        'C': '🇺🇸 Select the interface language:',
        'CH': '🇺🇸 You have changed the language to English',
        'L': '📃 Open the profile list to configure your profile.',
        'QF': 'Enter the minimum number of copies from which you want to start buying NFT gifts:',
        'QT': 'Enter the maximum number of copies up to which you want to buy NFT gifts:',
        'PF': 'Enter the price from which to start buying NFT gifts:',
        'PT': 'Enter the price up to which to buy NFT gifts:',
        'B': 'On your balance: {b} stars.\nProfile balance: {pb}\nEnter the amount you want to top up the profile balance with:',
        'PSD': '✅ Profile successfully deleted.',
        'CP': '🚫 Please enter a valid number to top up the profile balance.',
        'MP': '🚫 The minimum allowed amount to top up the profile balance is 1 star.',
        'NE': '🚫 Not enough stars on the balance to complete the operation.',
        'SP': '👌 The profile balance has been successfully topped up by {b} stars.',
        'CPF': '🚫 Please enter a valid number for the price from which you want to start buying NFT gifts.',
        'PI': '🎁 Quantity: specify the range — from how many to how many copies of fresh NFT gifts to buy.\n⭐️ Price: specify the range — from what to what price to buy fresh NFT gifts.',
        'MPN': '🚫 The minimum allowed price for buying NFT gifts is 0.',
        'CPT': '🚫 Please enter a valid number for the price up to which you want to buy NFT gifts.',
        'CST': '🚫 Please enter a valid number for the maximum number of copies up to which you want to buy NFT gifts.',
        'MSN': '🚫 The minimum allowed number of copies for buying NFT gifts is 0.',
        'CSF': '🚫 Please enter a valid number for the minimum number of copies from which you want to start buying NFT gifts.',
        'CS': '🚫 Please enter a valid number of stars.',
        'CD': '⭐ Top-Up.',
        'DT': 'Balance Top-Up.',
        'DI': '⭐ Balance top-up of {ge_am} stars.',
        'MS': '🚫 The minimum number of stars required for top-up is 50.',
        'PE': '🥹 No profiles left.',
        'YB': 'On your balance: {ub}',
        'YL': '📃 Your profile list:',
        'BSA': '🟢 Bot is on',
        'BSI': '🔴 Bot is off',
        'F': 'From:',
        'T': 'To:',
        'PBD': '⭐ Top Up Profile Balance',
        'PD': '🚫 Delete Profile',
        'BK': '🔙 Back',
        'UNF': '🤔 The user who invited you does not exist.',
        'NPA': '😡 No profiles available. Create at least one to continue.',
        'YG': '🎁 Your purchase list:',
        'HNP': '😭 You have no purchases.',
        'BGI': '🎁 NFT Gift: {stick}\n🌟 Price: {pr} stars.\n🕘 Purchase Date: {time}',
        'PHS': '⚠️ This profile had {pr} stars.\nThe specified amount has been returned to the balance.'
},
    'uk': {
        'H': 'Вітаю, {us}.\nЦей бот автоматично скуповує свіжі NFT-подарунки в Telegram. Основний функціонал:',
        'A': '⚡ Автопокупівля активується одразу після релізу нових NFT-подарунків.\nСпочатку можна створити до {q} профілів.\nЗалишилася кількість профілів: {s}.',
        'D': '🌟 Баланс: {b} зірок.\nПоповнення здійснюється у зірках.\nКомісія: 2%.\nМінімальне поповнення: 50 зірок.\nВкажіть кількість для поповнення:',
        'P':  '⚖ Історія ваших покупок:',
        'R': '👤 За кожні 3 запрошених користувачі надається 1 додатковий профіль.\nЗапрошено: {rs} користувачів.\nВаша реферальна посилання:\nhttps://t.me/FastGiftBuyerBot?start={r}',
        'C': '🇺🇦 Виберіть мову інтерфейсу:',
        'CH': '🇺🇦 Ви змінили мову на українську.',
        'L': '📃 Відкрийте список профілів, щоб виконати налаштування профілю.',
        'QF': 'Введіть, з якої кількості копій ви хочете почати скуповувати NFT-подарунки:',
        'QT': 'Введіть, до якої кількості копій ви хочете скуповувати NFT-подарунки:',
        'PF': 'Вкажіть ціну, з якої почати скуповування NFT-подарунків:',
        'PT': 'Вкажіть ціну, до якої скуповувати NFT-подарунки:',
        'B': 'На вашому балансі: {b} зірок.\nБаланс профілю: {pb}\nВведіть суму, на яку хочете поповнити баланс профілю:',
        'PSD': '✅ Профіль успішно видалено.',
        'CP': '🚫 Введіть коректне число для поповнення балансу профілю.',
        'MP': '🚫 Мінімально допустима сума поповнення балансу профілю — 1 зірка.',
        'NE': '🚫 Недостатньо зірок на балансі для виконання операції.',
        'SP': '👌 Баланс профілю успішно поповнено на {b} зірок.',
        'CPF': '🚫 Введіть коректне число, з якої ціни ви хочете почати скуповувати NFT-подарунки.',
        'PI': '🎁 Кількість: вкажіть діапазон — від якої до якої кількості копій свіжих NFT-подарунків скуповувати.\n⭐️ Ціна: вкажіть діапазон — від якої до якої ціни скуповувати свіжі NFT-подарунки.',
        'MPN': '🚫 Мінімально допустима ціна для скуповування NFT-подарунків - 0.',
        'CPT': '🚫 Введіть коректне число, до якої ціни ви хочете скуповувати NFT-подарунки.',
        'CST': '🚫 Введіть коректне число, до якої кількості копій ви хочете скуповувати NFT-подарунки.',
        'MSN': '🚫 Мінімально допустима кількість копій для скуповування NFT-подарунків: 0.',
        'CSF': '🚫 Введіть коректне число, з якої кількості копій ви хочете почати скуповувати NFT-подарунки.',
        'CS': '🚫 Введіть коректну кількість зірок.',
        'CD': '⭐ Поповнити',
        'DT': 'Поповнення балансу.',
        'DI': '⭐ Поповнення балансу на {ge_am} зірок.',
        'MS': '🚫 Мінімальна кількість зірок для поповнення: 50.',
        'PE': '🥹 Профілі закінчились.',
        'YB': 'На вашому балансі: {ub}',
        'YL': '📃 Ваш список профілів:',
        'BSA': '🟢 Бот увімкнено',
        'BSI': '🔴 Бот вимкнено',
        'F': 'Від:',
        'T': 'До:',
        'PBD': '⭐ Поповнити баланс профілю',
        'PD': '🚫 Видалити профіль',
        'BK': '🔙 Назад',
        'UNF': '🤔 Користувач, який вас запросив, не існує.',
        'NPA': '😡 Профілі відсутні. Створіть хоча б один, щоб продовжити.',
        'YG': '🎁 Ваш список покупок:',
        'HNP': '😭 У вас немає жодних покупок.',
        'BGI': '🎁NFT-подарунок: {stick}\n🌟Ціна: {pr} зірок.\n🕘Дата покупки: {time}',
        'PHS': '⚠️ У цьому профілі було {pr} зірок.\nВказану суму було повернено на баланс.'
}
}
keybos = {
    'ru': {
        'M': ru_main,
        'C': cr_prof_ru,
        'B': ru_back,
        'L': ru_lang
},
    'en': {
        'M': en_main,
        'C': cr_prof_en,
        'B': en_back,
        'L': en_lang
},
    'uk': {
        'M': uk_main,
        'C': cr_prof_uk,
        'B': uk_back,
        'L': uk_lang
    }
}