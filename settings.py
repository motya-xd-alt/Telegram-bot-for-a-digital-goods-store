
# Token telegran bot
bot_token = ''
CHANNEL_ID = 0 # Channel ID where the information will be sent, ID without -100 at the beginning (for example: 124873248) - specify instead of zero

# ID admin
admin_id = 0

bot_login = ''
ref_percent = 5 # Referral system percentage

QIWI_NUMBER = '+77777777777'
QIWI_TOKEN = 'token'

text_purchase = '❕ Вы выбрали: ' \
                '{name}\n\n' \
                '{info}\n\n' \
                '💠 Цена: {price} рублей\n' \
                '💠 Кол-во товара: {amount}' \


# инфа
info = '''❗️ Информация:\n'''

# Пополнение баланса
replenish_balance = '⚠️ Пополнение баланса\n\n' \
                    '🥝 Оплата киви: \n\n' \
                    '👉 Номер  {number}\n' \
                    '👉 Коментарий  {code}\n' \
                    '👉 Сумма  от 1 до 15000 рублей'

# Профиль
profile = '🧾 Профиль\n\n' \
          '❕ Ваш id - {id}\n' \
          '❕ Ваш логин - {login}\n' \
          '❕ Дата регистрации - {data}\n\n' \
          '💰 Ваш баланс - {balance} рублей'
