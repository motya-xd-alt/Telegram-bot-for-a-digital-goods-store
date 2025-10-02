from telebot import types


# Main menu
main_menu = types.InlineKeyboardMarkup(row_width=3)
main_menu.add(
    types.InlineKeyboardButton(text='🛍 Catalog', callback_data='catalog'),
    types.InlineKeyboardButton(text='👤 Profile', callback_data='profile'),
    types.InlineKeyboardButton(text='ℹ️ Info', callback_data='info'),
    types.InlineKeyboardButton(text='🛒 purchases', callback_data='purchases'),
    types.InlineKeyboardButton(text='💸 replenish_balance', callback_data='replenish_balance'),
)
main_menu.add(
    types.InlineKeyboardButton(text='👥 referral_web', callback_data='referral_web'),
)

# Admin menu
admin_menu = types.InlineKeyboardMarkup(row_width=2)
admin_menu.add(types.InlineKeyboardButton(text='catalog_control', callback_data='catalog_control'))
admin_menu.add(types.InlineKeyboardButton(text='section_control', callback_data='section_control'))
admin_menu.add(types.InlineKeyboardButton(text='give_balance', callback_data='give_balance'))
admin_menu.add(types.InlineKeyboardButton(text='admin_sending_messages', callback_data='admin_sending_messages'))
admin_menu.add(types.InlineKeyboardButton(text='admin_top_ref', callback_data='admin_top_ref'))
admin_menu.add(
    types.InlineKeyboardButton(text='Info', callback_data='admin_info'),
    types.InlineKeyboardButton(text='Exit', callback_data='exit_admin_menu')
)

# Admin control
admin_menu_control_catalog = types.InlineKeyboardMarkup(row_width=1)
admin_menu_control_catalog.add(
    types.InlineKeyboardButton(text='add_section_to_catalog', callback_data='add_section_to_catalog'),
    types.InlineKeyboardButton(text='del_section_to_catalog', callback_data='del_section_to_catalog'),
    types.InlineKeyboardButton(text='Back', callback_data='back_to_admin_menu')
)

# Admin control section
admin_menu_control_section = types.InlineKeyboardMarkup(row_width=1)
admin_menu_control_section.add(
    types.InlineKeyboardButton(text='add_product_to_section', callback_data='add_product_to_section'),
    types.InlineKeyboardButton(text='Удалить товар из раздела', callback_data='del_product_to_section'),
    types.InlineKeyboardButton(text='del_product_to_section', callback_data='download_product'),
    types.InlineKeyboardButton(text='Back', callback_data='back_to_admin_menu')
)

# Back to admin menu
back_to_admin_menu = types.InlineKeyboardMarkup(row_width=1)
back_to_admin_menu.add(
    types.InlineKeyboardButton(text='back_to_admin_menu', callback_data='back_to_admin_menu')
)

btn_purchase = types.InlineKeyboardMarkup(row_width=2)
btn_purchase.add(
    types.InlineKeyboardButton(text='Buy', callback_data='buy'),
    types.InlineKeyboardButton(text='Exit', callback_data='exit_to_menu')
)

btn_ok = types.InlineKeyboardMarkup(row_width=3)
btn_ok.add(
    types.InlineKeyboardButton(text='Ok', callback_data='btn_ok')
)

replenish_balance = types.InlineKeyboardMarkup(row_width=3)
replenish_balance.add(
    types.InlineKeyboardButton(text='🔄 Check', callback_data='check_payment'),
    types.InlineKeyboardButton(text='❌ Cancel', callback_data='cancel_payment')
)

to_close = types.InlineKeyboardMarkup(row_width=3)
to_close.add(
    types.InlineKeyboardButton(text='❌', callback_data='to_close')
)




