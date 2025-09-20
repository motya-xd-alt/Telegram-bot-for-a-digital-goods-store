#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import menu
import settings
import functions as func
import telebot
from telebot import types
import time
import datetime
import random

catalog_dict = {}
product_dict = {}
download_dict = {}
balance_dict = {}
admin_sending_messages_dict = {}

def start_bot():
    bot = telebot.TeleBot(settings.bot_token)

    # Command start
    @bot.message_handler(commands=['start'])
    def handler_start(message):
        chat_id = message.chat.id
        func.first_join(user_id=chat_id, name=message.from_user.username, code=message.text[6:])
        bot.send_message(chat_id,
                         'Welcome {}, user id - {}'.format(message.from_user.first_name,
                                                                    chat_id,),
                         reply_markup=menu.main_menu)

    # Command admin
    @bot.message_handler(commands=['admin'])
    def handler_admin(message):
        chat_id = message.chat.id
        if chat_id == settings.admin_id:
            bot.send_message(chat_id, 'You have entered the admin menu.', reply_markup=menu.admin_menu)

    # Обработка данных
    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        # Main menu
        if call.data == 'catalog':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='Каталог',
                reply_markup=func.menu_catalog()
            )

        if call.data == 'exit_from_catalog':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='You came back',
                reply_markup=menu.main_menu
            )


        if call.data in func.list_sections():
            name = call.data
            product = func.Product(chat_id)
            product_dict[call.message.chat.id] = product
            product.section = name

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'❕ Select the desired product',
                reply_markup=func.menu_section(call.data)
            )

        if call.data in func.list_product():
            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM "{call.data}"')
            row = cursor.fetchall()
            if len(row) > 0:
                product = func.Product(chat_id)
                product_dict[chat_id] = product
                product = product_dict[chat_id]

                info = func.menu_product(call.data, product)
                product.product = info[1].product
                product.section = info[1].section
                product.amount_MAX = info[1].amount_MAX
                product.price = info[1].price

                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=info[0],
                    reply_markup=menu.btn_purchase
                )

            if len(row) == 0:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='This item is out of stock. Please contact technical support.',
                    reply_markup=menu.main_menu
                )

        if call.data == 'buy':
            try:
                product = product_dict[chat_id]
                msg = bot.send_message(chat_id=chat_id,
                                       text=f'❕ Enter the quantity of the product\n❕ От 1 - {product.amount_MAX}')
                bot.register_next_step_handler(msg, buy)
            except:
                pass
                
        if call.data == 'info':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=settings.info,
                reply_markup=menu.main_menu
            )

        if call.data == 'purchases':
            msg = func.basket(chat_id)
            if len(msg) > 0:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=msg,
                                      reply_markup=menu.main_menu)
            if len(msg) == 0:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text='You have no purchases 😢',
                                      reply_markup=menu.main_menu)


        if call.data == 'exit_to_menu':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='You have returned to the main menu.',
                reply_markup=menu.main_menu
            )

        if call.data == 'btn_ok':
            bot.delete_message(chat_id, message_id)

        if call.data == 'profile':
            info = func.profile(chat_id)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=settings.profile.format(
                                      id=info[0],
                                      login=f'@{info[1]}',
                                      data=info[2][:19],
                                      balance=info[5]
                                  ),
                                  reply_markup=menu.main_menu)

        # Admin menu
        if call.data == 'admin_info':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=func.admin_info(),
                reply_markup=menu.admin_menu
            )

        if call.data == 'add_section_to_catalog':
            if chat_id == settings.admin_id:
                msg = bot.send_message(chat_id=chat_id,
                                       text='Enter the section name')
                bot.register_next_step_handler(msg, create_section)

        if call.data == 'del_section_to_catalog':
            if chat_id == settings.admin_id:
                conn = sqlite3.connect("base_ts.sqlite")
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM catalog')
                row = cursor.fetchall()
                cursor.close()
                conn.close()

                text = ''
                num = 0

                for i in row:
                    text = text + '№ ' + str(num) + '   |  ' + str(i[0]) + '\n'
                    num += 1

                msg = bot.send_message(
                    chat_id=chat_id,
                    text='Enter the section number\n\n'
                         f'{text}'
                )
                bot.register_next_step_handler(msg, del_section)

        if call.data == 'add_product_to_section':
            if chat_id == settings.admin_id:
                conn = sqlite3.connect("base_ts.sqlite")
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM catalog')
                row = cursor.fetchall()

                text = ''
                num = 0

                for i in row:
                    text = text + '№ ' + str(num) + '   |  ' + str(i[0]) + '\n'
                    num += 1

                msg = bot.send_message(chat_id=chat_id,
                                       text='Enter the section number to which you want to add the product.\n\n'
                                            f'{text}')
                bot.register_next_step_handler(msg, create_product)

        if call.data == 'del_product_to_section':
            if chat_id == settings.admin_id:
                conn = sqlite3.connect("base_ts.sqlite")
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM catalog')
                row = cursor.fetchall()

                text = ''
                num = 0

                for i in row:
                    text = text + '№ ' + str(num) + '   |  ' + str(i[0]) + '\n'
                    num += 1

                msg = bot.send_message(chat_id=chat_id,
                                       text='Enter the section number from which you want to remove the product.\n\n'
                                            f'{text}')
                bot.register_next_step_handler(msg, del_product)

        if call.data == 'download_product':
            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM catalog')
            row = cursor.fetchall()

            text = ''
            num = 0

            for i in row:
                text = text + '№ ' + str(num) + '   |  ' + str(i[0]) + '\n'
                num += 1

            msg = bot.send_message(chat_id=chat_id,
                                   text='Enter the section number\n\n'
                                        f'{text}')
            bot.register_next_step_handler(msg, download_product)

        if call.data == 'exit_admin_menu':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='You have left the admin menu.',
                reply_markup=menu.main_menu
            )

        if call.data == 'back_to_admin_menu':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='You have entered the admin menu.',
                reply_markup=menu.admin_menu
            )

        if call.data == 'catalog_control':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='You have entered the directory management',
                reply_markup=menu.admin_menu_control_catalog
            )

        if call.data == 'section_control':
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='You have entered the section management',
                reply_markup=menu.admin_menu_control_section
            )

        if call.data == 'replenish_balance':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=func.replenish_balance(chat_id),
                                  reply_markup=menu.replenish_balance)

        if call.data == 'cancel_payment':
            func.cancel_payment(chat_id)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='❕ Welcome',
                                  reply_markup=menu.main_menu)

        if call.data == 'check_payment':
            check = func.check_payment(chat_id)
            if check[0] == 1:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=f'✅ Payment completed\nAmount - {check[1]} руб',
                                      reply_markup=menu.main_menu)

                bot.send_message(chat_id=settings.admin_id,
                                 text='💰 Balance replenishment\n'
                                      f'🔥 От - {chat_id}\n'
                                      f'🔥 Sum - {check[1]} dol')

                try:
                    bot.send_message(chat_id=f'-100{settings.CHANNEL_ID}',
                                     text='💰 Balance replenishment\n'
                                          f'🔥 От - {chat_id}\n'
                                          f'🔥 Sum - {check[1]} dol')
                except: pass

            if check[0] == 0:
                bot.send_message(chat_id=chat_id,
                                 text='❌ Payment not found',
                                 reply_markup=menu.to_close)

        if call.data == 'to_close':
            bot.delete_message(chat_id=chat_id,
                               message_id=message_id)

        if call.data == 'give_balance':
            msg = bot.send_message(chat_id=chat_id,
                                   text='Enter the ID of the person whose balance will be changed')

            bot.register_next_step_handler(msg, give_balance)

        if call.data == 'admin_sending_messages':
            msg = bot.send_message(chat_id,
                                   text='Enter the text of the newsletter')
            bot.register_next_step_handler(msg, admin_sending_messages)

        if call.data == 'referral_web':
            ref_code = func.check_ref_code(chat_id)
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'👥 Referral network\n\n'
                     f'Your referral link:\n'
                     f'https://teleg.run/{settings.bot_login}?start={ref_code}\n\n'
                     f'Over the entire period you have earned - {func.check_all_profit_user(chat_id)} ₽\n\n'
                     f'<i>If a person invited via your referral link tops up their balance, you will receive {settings.ref_percent}% of their deposit amount.</i>',
                reply_markup=menu.main_menu,
                parse_mode='html'
                )
        
        if call.data == 'admin_top_ref':
            bot.send_message(
                chat_id=chat_id,
                text=func.admin_top_ref(),
                parse_mode='html'
            )


    def give_balance(message):
        try:
            balance = func.GiveBalance(message.text)
            balance_dict[message.chat.id] = balance

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Enter the amount by which the balance will change (this amount will not be added to the balance, but the balance will change by it)')

            bot.register_next_step_handler(msg, give_balance_2)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Something didnt go according to plan',
                             reply_markup=menu.main_menu)

    def give_balance_2(message):
        try:
            balance = balance_dict[message.chat.id]
            balance.balance = message.text
            code = random.randint(111, 999)
            balance.code = code
            msg = bot.send_message(chat_id=message.chat.id,
                                   text=f'ID - {balance.login}\n'
                                        f'The balance will change to - {balance.balance}\n'
                                        f'To confirm, please enter {code}')

            bot.register_next_step_handler(msg, give_balance_3)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Something didnt go according to plan',
                             reply_markup=menu.main_menu)

    def give_balance_3(message):
        try:
            balance = balance_dict[message.chat.id]
            if int(message.text) == balance.code:
                func.give_balance(balance)
                bot.send_message(chat_id=message.chat.id,
                                 text='✅ Balance changed successfully')
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Something didnt go according to plan',
                             reply_markup=menu.main_menu)

    def create_section(message):
        try:
            name = message.text
            catalog = func.Catalog(name)
            catalog_dict[message.chat.id] = catalog
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Yes', 'No')
            msg = bot.send_message(chat_id=message.chat.id,
                                   text=name + '\n\n Create?',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, create_section_2)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Something didnt go according to plan',
                             reply_markup=menu.main_menu)

    def buy(message):
        try:
            product = product_dict[message.chat.id]
            if int(message.text) in range(1, int(product.amount_MAX)+1):
                product.amount = int(message.text)

                code = random.randint(111, 999)
                product.code = code

                msg = bot.send_message(chat_id=message.chat.id,
                    text=f'❕ You have chosen - {product.product}\n'
                       f'❕ Кол-во - {product.amount}\n'
                       f'❕ Price - {float(product.price) * int(product.amount)} руб\n'
                       f'👉 To confirm your purchase, please send {code}')
                bot.register_next_step_handler(msg, buy_2)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='❌ Incorrect quantity',
                                 reply_markup=menu.main_menu)
        except:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Something didnt go according to plan',
                             reply_markup=menu.main_menu)

    def buy_2(message):
        try:
            product = product_dict[message.chat.id]
            if int(message.text) == product.code:
                check = func.check_balance(product.user_id, (float(product.price)*int(product.amount)))

                if check == 1:

                    list = func.buy(product)
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'✅ You have successfully purchased the product.\n\n{list}',
                                     reply_markup=menu.main_menu)

                    bot.send_message(chat_id=settings.admin_id,
                                     text=f'✅ Product purchased\n\n'
                                          f'❕ Purchased by - {message.chat.id}\n'
                                          f'❕ Purchase amount - {float(product.price) * int(product.amount)}\n'
                                          f'❕ Purchase date - {datetime.datetime.now()}\n'
                                          f'❕ Purchased product ⬇️\n\n{list}')

                    try:
                        bot.send_message(chat_id=f'-100{settings.CHANNEL_ID}',
                                         text=f'✅ Product purchased\n\n'
                                              f'❕ Purchased by - {message.chat.id}\n'
                                              f'❕ Purchase amount - {float(product.price) * int(product.amount)}\n'
                                              f'❕ Purchase date - {datetime.datetime.now()}\n'
                                              f'❕ Purchased product ⬇️\n\n{list}')

                    except: pass

                if check == 0:
                    bot.send_message(chat_id=message.chat.id,
                                     text='❌ There are insufficient funds on the balance')

            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='❌ Purchase canceled',
                                 reply_markup=menu.main_menu)
        except:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Something didnt go according to plan',
                             reply_markup=menu.main_menu)

    def create_section_2(message):
        try:
            if message.text == 'Yes':
                catalog = catalog_dict[message.chat.id]
                func.add_section_to_catalog(catalog.name)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'✅Section: {catalog.name}\n'
                         f'✅Successfully added to the catalog',
                    reply_markup=menu.admin_menu
                )
        except Exception as e:
            print(e)

    def del_section(message):
        try:
            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM catalog')
            row = cursor.fetchall()
            cursor.close()
            conn.close()

            name = row[int(message.text)][1]
            nm = row[int(message.text)][0]
            num_catalog = func.Catalog(name)
            catalog_dict[message.chat.id] = num_catalog

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Yes', 'No')

            msg = bot.send_message(chat_id=message.chat.id,
                                   text=f'{nm}\nУдалить этот каталог?',
                                   reply_markup=markup)

            bot.register_next_step_handler(msg, del_section_2)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Упсс, что-то пошло не по плану')

    def del_section_2(message):
        try:
            if message.text == 'Yes':
                catalog = catalog_dict[message.chat.id]
                func.del_section_to_catalog(catalog.name)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'✅Section: {catalog.name}\n'
                         f'✅Successfully added to the catalog',
                    reply_markup=menu.admin_menu
                )
            if message.text == 'No':
                bot.send_message(chat_id=message.chat.id,
                                 text='You have returned to the admin menu.',
                                 reply_markup=menu.admin_menu)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def create_product(message):
        try:
            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM catalog')
            row = cursor.fetchall()
            cursor.close()
            conn.close()

            name = row[int(message.text)][1]
            num_catalog = func.Product(name)
            product_dict[message.chat.id] = num_catalog

            addproduct = product_dict[message.chat.id]
            addproduct.section = name

            msg = bot.send_message(chat_id=message.chat.id,
                                   text=f'{name}\nEnter the product name')

            bot.register_next_step_handler(msg, create_product_2)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def create_product_2(message):
        try:
            product_name = message.text
            product = product_dict[message.chat.id]
            product.product = product_name

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Enter product prices')
            bot.register_next_step_handler(msg, create_product_3)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def create_product_3(message):
        try:
            price = message.text
            product = product_dict[message.chat.id]
            product.price = price

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Enter a product description')

            bot.register_next_step_handler(msg, create_product_4)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def create_product_4(message):
        try:
            product = product_dict[message.chat.id]
            product.info = message.text

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Yes', 'No')

            product_name = f'{product.product} | {product.price} руб'
            msg = bot.send_message(chat_id=message.chat.id,
                                   text=f'{product_name}\n\n'
                                        'Create?',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, create_product_5)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def create_product_5(message):
        try:
            if message.text == 'Yes':
                product = product_dict[message.chat.id]
                product_name = f'{product.product} | {product.price} руб'

                func.add_product_to_section(product_name, product.price, product.section, product.info)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'✅Product: {product_name}\n'
                         f'✅Successfully added to the section',
                    reply_markup=menu.admin_menu
                )
        except Exception as e:
            print(e)
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def del_product(message):
        try:
            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM catalog')
            row = cursor.fetchall()
            cursor.close()
            conn.close()

            name = row[int(message.text)][1]
            product = func.AddProduct(name)
            product_dict[message.chat.id] = product

            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM "{name}"')
            row = cursor.fetchall()
            cursor.close()
            conn.close()

            text = ''
            num = 0

            for i in row:
                text = text + '№ ' + str(num) + '   |  ' + str(i[0]) + '\n'
                num += 1

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Select the product number you want to delete.\n\n'
                                        f'{text}')
            bot.register_next_step_handler(msg, del_product_2)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def del_product_2(message):
        try:
            product = product_dict[message.chat.id]

            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM '{product.section}'")
            row = cursor.fetchall()

            name_product = row[int(message.text)][0]
            product.product = name_product

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Yes', 'No')

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='❕Delete ⬇️\n'
                                        f'❕{product.product}\n\n'
                                        '❕from the section ⬇️\n'
                                        f'❕{product.section}  ?',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, del_product_3)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def del_product_3(message):
        try:
            if message.text == 'Yes':
                product = product_dict[message.chat.id]

                func.del_product_to_section(product.product, product.section)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'✅Product: {product.product}\n'
                         f'✅Successfully removed from section',
                    reply_markup=menu.admin_menu
                )
            if message.text == 'No':
                bot.send_message(chat_id=message.chat.id,
                                 text='You have returned to the admin menu.',
                                 reply_markup=menu.admin_menu)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def download_product(message):
        try:
            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM catalog')
            row = cursor.fetchall()

            name_section = row[int(message.text)][1]
            download = func.DownloadProduct(name_section)
            download_dict[message.chat.id] = download

            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM "{name_section}"')
            row = cursor.fetchall()

            cursor.close()
            conn.close()

            text = ''
            num = 0

            for i in row:
                text = text + '№ ' + str(num) + '   |  ' + str(i[0]) + '\n'
                num += 1

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Select product number\n\n'
                                        f'{text}')

            bot.register_next_step_handler(msg, download_product_2)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def download_product_2(message):
        try:
            product = download_dict[message.chat.id]

            conn = sqlite3.connect("base_ts.sqlite")
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM "{product.name_section}"')
            row = cursor.fetchall()

            product.name_product = row[int(message.text)][2]

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Yes', 'No')

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Do you want to add a product to ⬇️\n\n'
                                        f'ID - {product.name_product}',
                                   reply_markup=markup)

            bot.register_next_step_handler(msg, download_product_3)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def download_product_3(message):
        try:
            if message.text == 'Yes':
                msg = bot.send_message(chat_id=message.chat.id,
                                       text='❕Отправьте txt файл с товаром\n\n'
                                            '❗️ 1 строчка = 1 товару!!!\n\n'
                                            '❗️ ПРИМЕР ФАЙЛА:\n'
                                            'main@mail.ru:password\n'
                                            'QWERT-QWERY-QWERY\n'
                                            'какая-то_ссылка.ru')

                bot.register_next_step_handler(msg, download_product_4)

            if message.text == 'No':
                bot.send_message(chat_id=message.chat.id,
                                 text='Вы вернулись в меню админа',
                                 reply_markup=menu.admin_menu)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

    def admin_sending_messages(message):
        dict = func.Admin_sending_messages(message.chat.id)
        admin_sending_messages_dict[message.chat.id] = dict

        dict = admin_sending_messages_dict[message.chat.id]
        dict.text = message.text

        msg = bot.send_message(message.chat.id,
                               text='Отправьте "ПОДТВЕРДИТЬ" для подтверждения')
        bot.register_next_step_handler(msg, admin_sending_messages_2)

    def admin_sending_messages_2(message):
        conn = sqlite3.connect('base_ts.sqlite')
        cursor = conn.cursor()
        dict = admin_sending_messages_dict[message.chat.id]
        if message.text == 'ПОДТВЕРДИТЬ':
            cursor.execute(f'SELECT * FROM users')
            row = cursor.fetchall()

            for i in range(len(row)):
                try:
                    time.sleep(1)
                    bot.send_message(row[i][0], dict.text)

                except:
                    pass
        else:
            bot.send_message(message.chat.id, text='Рассылка отменена')

    @bot.message_handler(content_types=['document'])
    def download_product_4(message):
        try:
            chat_id = message.chat.id
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            download = download_dict[message.chat.id]

            with open(message.document.file_name, 'wb') as doc:
                doc.write(downloaded_file)

            func.download_product(message.document.file_name, download.name_product)

            bot.send_message(chat_id=chat_id,
                             text='❕ Товар загружен 👍')
        except Exception as e:
            pass
            bot.send_message(chat_id=message.chat.id,
                             text='Oops, something didnt go according to plan.')

            


    bot.polling(none_stop=True)



start_bot()
