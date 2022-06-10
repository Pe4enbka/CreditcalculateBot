from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnBack = InlineKeyboardButton(text='Назад', callback_data='btn_back')
btnMainMenu = InlineKeyboardButton(text='Главная', callback_data='btn_main_menu')
btnBackEntity = InlineKeyboardButton(text='Назад', callback_data='btn_back_entity')

btnRegistration = InlineKeyboardButton(text='Регистрация', callback_data='btn_reg')
btnLook = InlineKeyboardButton(text='Посмотреть', callback_data='btn_look')
btnCalculator = InlineKeyboardButton(text='Калькулятор', callback_data='btn_calculator')
startMenu = InlineKeyboardMarkup(row_width=2)
btnBackStart = InlineKeyboardButton(text='Назад', callback_data='btn_back_start')

btnIndividual = InlineKeyboardButton(text='Физицеское лицо', callback_data='btn_individual')
btnEntity = InlineKeyboardButton(text='Юридическое лицо', callback_data='btn_entity')
roleMenu = InlineKeyboardMarkup(row_width=2)

btnFullName = InlineKeyboardButton(text='ФИО', callback_data='btn_fullName')
btnAge = InlineKeyboardButton(text='Дата рождения', callback_data='btn_age')
btnNationality = InlineKeyboardButton(text='Национальность', callback_data='btn_nationality')
btnSalary = InlineKeyboardButton(text='Зарплата', callback_data='btn_salary')
btnPassport = InlineKeyboardButton(text='Паспортные данные', callback_data='btn_passport')
individualMenu = InlineKeyboardMarkup(row_width=2)

btnName = InlineKeyboardButton(text='Имя', callback_data='btn_name')
btnLastName = InlineKeyboardButton(text='Фамилия', callback_data='btn_lastName')
fullNameMenu = InlineKeyboardMarkup(row_width=1)

btnEntityTime = InlineKeyboardButton(text='Начало фин. деятельности', callback_data='btn_entity_time')
btnEntityActive = InlineKeyboardButton(text='Активы', callback_data='btn_entity_active')
entityMenu = InlineKeyboardMarkup(row_width=1)

btnActiveAdd = InlineKeyboardButton(text='Добавить', callback_data='btn_active_add')
btnActiveView = InlineKeyboardButton(text='Посмотреть', callback_data='btn_active_view')
activeMenu = InlineKeyboardMarkup(row_width=1)

btnCondition = InlineKeyboardButton(text='Условия', callback_data='btn_condition')
btnCalcul = InlineKeyboardButton(text='Посчитать', callback_data='btn_calcul')
calculatorMenu = InlineKeyboardMarkup(row_width=1)

btnSber = InlineKeyboardButton(text='Сбер', callback_data='btn_sber')
btnTinkoff = InlineKeyboardButton(text='Тинькофф', callback_data='btn_tinkoff')
btnSovcom = InlineKeyboardButton(text='СовкомБанк', callback_data='btn_sovcom')
bankMenu = InlineKeyboardMarkup(row_width=1)

btnBankIndividual = InlineKeyboardButton(text='Физицеское лицо', callback_data='btn_bank_individual')
btnBankEntity = InlineKeyboardButton(text='Юридическое лицо', callback_data='btn_bank_entity')
btnBankBack = InlineKeyboardButton(text='Назад', callback_data='btn_bank_back')
roleBankMenu = InlineKeyboardMarkup(row_width=2)

btnConsumerCredit = InlineKeyboardButton(text='Потребительский кредит', callback_data='btn_consumer_credit')
btnMortgage = InlineKeyboardButton(text='Ипотечный кредит', callback_data='btn_mortgage')
btnCarLoan = InlineKeyboardButton(text='Автокредит', callback_data='btn_car_loan')
btnCreditCart = InlineKeyboardButton(text='Кредитные карты', callback_data='btn_credit_cart')
btnSocialCredit = InlineKeyboardButton(text='Социальный кредит', callback_data='btn_social_credit')
individualCreditMenu = InlineKeyboardMarkup(row_width=1)

btnSingleLoan = InlineKeyboardButton(text='Разовый заем', callback_data='btn_single_loan')
btnCreditLine = InlineKeyboardButton(text='Кркдитная линия', callback_data='btn_credit_line')
btnOverdraft = InlineKeyboardButton(text='Овердрафт', callback_data='btn_overdraft')
btnInvestmentLoan = InlineKeyboardButton(text='Инвестиционный заем', callback_data='btn_investment_loan')
btnCommercialMortgage = InlineKeyboardButton(text='Коммерческая ипотека', callback_data='btn_commercial_mortgage')
btnLeasing = InlineKeyboardButton(text='Лизинг', callback_data='btn_leasing')
entityCreditMenu = InlineKeyboardMarkup(row_width=1)

btnSend = InlineKeyboardButton(text='Отправить данные в банк', callback_data='btn_send')
sendMenu = InlineKeyboardMarkup(row_width=1)

startMenu.insert(btnRegistration)
startMenu.insert(btnLook)
startMenu.insert(btnCalculator)

roleMenu.insert(btnIndividual)
roleMenu.insert(btnEntity)
roleMenu.insert(btnBackStart)

individualMenu.insert(btnFullName)
individualMenu.insert(btnAge)
individualMenu.insert(btnNationality)
individualMenu.insert(btnSalary)
individualMenu.insert(btnPassport)
individualMenu.insert(btnMainMenu)

fullNameMenu.insert(btnName)
fullNameMenu.insert(btnLastName)
fullNameMenu.insert(btnBack)

entityMenu.insert(btnEntityTime)
entityMenu.insert(btnEntityActive)
entityMenu.insert(btnMainMenu)

activeMenu.insert(btnActiveAdd)
activeMenu.insert(btnActiveView)
activeMenu.insert(btnBackEntity)

calculatorMenu.insert(btnCondition)
calculatorMenu.insert(btnCalcul)
calculatorMenu.insert(btnMainMenu)

bankMenu.insert(btnSber)
bankMenu.insert(btnTinkoff)
bankMenu.insert(btnSovcom)
bankMenu.insert(btnMainMenu)

roleBankMenu.insert(btnBankIndividual)
roleBankMenu.insert(btnBankEntity)
roleBankMenu.insert(btnBankBack)

individualCreditMenu.insert(btnConsumerCredit)
individualCreditMenu.insert(btnMortgage)
individualCreditMenu.insert(btnCarLoan)
individualCreditMenu.insert(btnCreditCart)
individualCreditMenu.insert(btnSocialCredit)
individualCreditMenu.insert(btnBankBack)

entityCreditMenu.insert(btnSingleLoan)
entityCreditMenu.insert(btnCreditLine)
entityCreditMenu.insert(btnOverdraft)
entityCreditMenu.insert(btnInvestmentLoan)
entityCreditMenu.insert(btnCommercialMortgage)
entityCreditMenu.insert(btnLeasing)
entityCreditMenu.insert(btnBankBack)

sendMenu.insert(btnSend)
sendMenu.insert(btnBankBack)