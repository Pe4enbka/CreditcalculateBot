from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnBack = InlineKeyboardButton(text='Назад', callback_data='btn_back')

btnRegistration = InlineKeyboardButton(text='Регистрация', callback_data='btn_reg')
btnLook = InlineKeyboardButton(text='Посмотреть', callback_data='btn_look')
startMenu = InlineKeyboardMarkup(row_width=2)

btnIndividual = InlineKeyboardButton(text='Физицеское лицо', callback_data='btn_individual')
btnEntity = InlineKeyboardButton(text='Юридическое лицо', callback_data='btn_entity')
roleMenu = InlineKeyboardMarkup(row_width=2)

btnFullName = InlineKeyboardButton(text='ФИО', callback_data='btn_fullName')
btnAge = InlineKeyboardButton(text='Дата рождения', callback_data='btn_age')
btnNationality = InlineKeyboardButton(text='Национальность', callback_data='btn_nationality')
btnSalary = InlineKeyboardButton(text='Зарплата', callback_data='btn_salary')
individualMenu = InlineKeyboardMarkup(row_width=2)

btnName = InlineKeyboardButton(text='Имя', callback_data='btn_name')
btnLastName = InlineKeyboardButton(text='Фамилия', callback_data='btn_lastName')
btnPatronymic = InlineKeyboardButton(text='Отчество', callback_data='btn_patronymic')
fullNameMenu = InlineKeyboardMarkup(row_width=1)

startMenu.insert(btnRegistration)
startMenu.insert(btnLook)

roleMenu.insert(btnIndividual)
roleMenu.insert(btnEntity)
roleMenu.insert(btnBack)

individualMenu.insert(btnFullName)
individualMenu.insert(btnAge)
individualMenu.insert(btnNationality)
individualMenu.insert(btnSalary)

fullNameMenu.insert(btnName)
fullNameMenu.insert(btnLastName)
fullNameMenu.insert(btnPatronymic)



