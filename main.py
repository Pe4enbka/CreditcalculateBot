import logging
import psycopg2
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import markup as nav
from config import *

flag = False
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
bank = None

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()


# старт бота
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.username}!'.format(message.from_user),
                           reply_markup=nav.startMenu)


####### машина состояний###############

class FSMName(StatesGroup):
    name = State()
    lastName = State()


class FSMDate(StatesGroup):
    date = State()
    month = State()
    year = State()


class FSMDate2(StatesGroup):
    date = State()
    month = State()
    year = State()


class FSMNationality(StatesGroup):
    nationality = State()


class FSMSalary(StatesGroup):
    salary = State()


class FSMPassport(StatesGroup):
    series = State()
    number = State()


class FSMActive(StatesGroup):
    new = State()


class FSMSalaryCredit(StatesGroup):
    salary = State()
    age = State()


##########################################


################# главное окно ##################

# регистрация в боте
@dp.callback_query_handler(text='btn_reg')
async def register(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    global flag
    flag = True
    await bot.send_message(message.from_user.id, 'Выберите вашу роль', reply_markup=nav.roleMenu)


# постотреть
@dp.callback_query_handler(text='btn_look')
async def look(message: types.Message):
    global flag
    flag = False
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите вашу роль', reply_markup=nav.roleMenu)


####################################################

################# выбор роли ##################

# вернуться назад
@dp.callback_query_handler(text='btn_back_start')
async def back(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Привет {0.username}!'.format(message.from_user),
                           reply_markup=nav.startMenu)


@dp.callback_query_handler(text='btn_back')
async def back(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)


@dp.callback_query_handler(text='btn_back_entity')
async def back(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.entityMenu)


# физическое лицо
@dp.callback_query_handler(text='btn_individual')
async def individual_role(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    user_id = message.from_user.id
    db_object.execute(f"SELECT id FROM individual WHERE id = {user_id}")
    result = db_object.fetchone()
    if flag:
        if not result:
            db_object.execute(f"INSERT INTO individual(id) VALUES (%s)", [user_id])
            db_connection.commit()

        await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)
    else:
        if not result:
            await bot.send_message(message.from_user.id, 'Вы не зарегистрированы', reply_markup=nav.roleMenu)
        else:
            await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)


@dp.callback_query_handler(text='btn_main_menu')
async def back(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Привет {0.username}!'.format(message.from_user),
                           reply_markup=nav.startMenu)


########################## имя

@dp.callback_query_handler(text='btn_fullName')
async def full_name(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.fullNameMenu)


@dp.callback_query_handler(text='btn_name', state=None)
async def name(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите имя')
        await FSMName.name.set()
    else:
        db_object.execute(f"SELECT name FROM individual")
        result = db_object.fetchone()
        name = 'Ваше имя: ' + ''.join(result)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.fullNameMenu)


@dp.message_handler(state=FSMName.name)
async def set_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.text

    db_object.execute(f"SELECT name FROM individual WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(name) VALUES (%s)", [user_name])
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE individual SET name = (%s)", [user_name])
        db_connection.commit()

    # await bot.delete_message(message.from_user.id, message.message.message_id)
    await state.finish()
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.fullNameMenu)


@dp.callback_query_handler(text='btn_lastName')
async def last_name(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите фамилию')
        await FSMName.name.set()
    else:
        db_object.execute(f"SELECT last_name FROM individual")
        result = db_object.fetchone()
        name = 'Ваша фамилия: ' + ''.join(result)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.fullNameMenu)


@dp.message_handler(state=FSMName.lastName)
async def set_lastname(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.text
    db_object.execute(f"SELECT last_name FROM individual WHERE id = {user_id}")

    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(last_name) VALUES (%s)", [user_name])
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE individual SET last_name = (%s)", [user_name])
        db_connection.commit()
    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.fullNameMenu)


###### дата рождения

@dp.callback_query_handler(text='btn_age')
async def age(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите число')
        await FSMDate.date.set()
    else:
        db_object.execute(f"SELECT to_char (age,'dd-mm-yyyy') FROM individual")
        result = db_object.fetchone()
        name = 'Ваша дата рождения: ' + ''.join(result)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)


@dp.message_handler(lambda message: not message.text.isdigit(), state=FSMDate)
async def process_age_invalid(message: types.Message):
    return await message.reply("Проверте корректность и посвторите ввод. Ввод должен осуществляться цифрами")


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMDate.date)
async def process_date(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    async with state.proxy() as data:
        data['date'] = message.text

    await FSMDate.next()
    await bot.send_message(message.from_user.id, 'Введите месяц')


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMDate.month)
async def process_month(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    async with state.proxy() as data:
        data['month'] = message.text

    await FSMDate.next()
    await bot.send_message(message.from_user.id, 'Введите год')


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMDate.year)
async def process_year(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    async with state.proxy() as data:
        data['year'] = message.text

        user_id = message.from_user.id
        user_date = data['year'] + '-' + data['month'] + '-' + data['date']
        db_object.execute(f"SELECT age FROM individual WHERE id = {user_id}")

        result = db_object.fetchone()

        if not result:
            db_object.execute(f"INSERT INTO individual(age) VALUES (%s)", [user_date])
            db_connection.commit()
        else:
            db_object.execute(f"UPDATE individual SET age = (%s)", [user_date])
            db_connection.commit()

    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)


####### нацональность

@dp.callback_query_handler(text='btn_nationality')
async def nationality(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите свою национальность')
        await FSMNationality.nationality.set()
    else:
        db_object.execute(f"SELECT nationality FROM individual")
        result = db_object.fetchone()
        name = 'Ваша национальность: ' + ''.join(result)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.individualMenu)


@dp.message_handler(state=FSMNationality.nationality)
async def set_nationality(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_nationality = message.text
    db_object.execute(f"SELECT nationality FROM individual WHERE id = {user_id}")

    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(nationality) VALUES (%s)", [user_nationality])
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE individual SET nationality = (%s)", [user_nationality])
        db_connection.commit()
    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.individualMenu)


####### зарплата

@dp.callback_query_handler(text='btn_salary')
async def salary(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите свою зарплату')
        await FSMSalary.salary.set()
    else:
        db_object.execute(f"SELECT to_char (salary,'L99999999999') FROM individual")
        result = db_object.fetchone()
        name = 'Ваша зарплата: ' + ''.join(result)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.individualMenu)


@dp.message_handler(state=FSMSalary.salary)
async def set_salary(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_salary = message.text
    db_object.execute(f"SELECT salary FROM individual WHERE id = {user_id}")

    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(salary) VALUES (%s)", [user_salary])
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE individual SET salary = (%s)", [user_salary])
        db_connection.commit()
    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.individualMenu)


@dp.callback_query_handler(text='btn_passport')
async def passport(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите серию')
        await FSMPassport.series.set()

    else:
        db_object.execute(f"SELECT to_char (series,'9999') FROM passport")
        result = db_object.fetchone()
        db_object.execute(f"SELECT to_char (number,'999999') FROM passport")
        num = db_object.fetchone()
        name = 'Ваш паспорт: ' + ''.join(result) + ' ' + ''.join(num)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.individualMenu)


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMPassport.series)
async def process_series(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['series'] = message.text

    await FSMPassport.next()
    await bot.send_message(message.from_user.id, 'Введите номер')


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMPassport.number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
        db_object.execute(f"SELECT id FROM passport")

        result = db_object.fetchone()

        if not result:
            db_object.execute(f"INSERT INTO passport(series,number) VALUES (%s, %s)", tuple(data.values()))
            db_object.execute(f"INSERT INTO individual(passport_id) VALUES (%s)", result)
            db_connection.commit()
        else:
            db_object.execute(f"UPDATE passport SET series = (%s), number = (%s)", tuple(data.values()))
            db_object.execute(f"UPDATE individual SET passport_id = (%s)", result)
            db_connection.commit()

    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)


########## юр лицо

@dp.callback_query_handler(text='btn_entity')
async def entity_role(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.entityMenu)


######## начало деятельностт

@dp.callback_query_handler(text='btn_entity_time')
async def age(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if flag:
        await bot.send_message(message.from_user.id, 'Введите число')
        await FSMDate2.date.set()
    else:
        db_object.execute(f"SELECT to_char (time,'dd-mm-yyyy') FROM entity")
        result = db_object.fetchone()
        name = 'Вы работаете с ' + ''.join(result)
        await bot.send_message(message.from_user.id, name)
        await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.entityMenu)


@dp.message_handler(lambda message: not message.text.isdigit(), state=FSMDate2)
async def process_age_invalid(message: types.Message):
    return await message.reply("Проверте корректность и посвторите ввод. Ввод должен осуществляться цифрами")


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMDate2.date)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

    await FSMDate2.next()
    await bot.send_message(message.from_user.id, 'Введите месяц')


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMDate2.month)
async def process_month(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = message.text

    await FSMDate2.next()
    await bot.send_message(message.from_user.id, 'Введите год')


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMDate2.year)
async def process_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = message.text

        user_date = data['year'] + '-' + data['month'] + '-' + data['date']
        db_object.execute(f"SELECT id FROM entity")

        result = db_object.fetchone()

        if not result:
            db_object.execute(f"INSERT INTO entity(time) VALUES (%s)", [user_date])
            db_connection.commit()
        else:
            db_object.execute(f"UPDATE entity SET time = (%s)", [user_date])
            db_connection.commit()

    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.entityMenu)


###### активы

@dp.callback_query_handler(text='btn_entity_active')
async def active(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.activeMenu)


@dp.callback_query_handler(text='btn_active_add')
async def active_add(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Введите новый актив')
    await FSMActive.new.set()


@dp.message_handler(state=FSMActive.new)
async def process_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new'] = message.text
        db_object.execute(f"SELECT active FROM entity")

        result = db_object.fetchone()

        if not result:
            db_object.execute(f"INSERT INTO entity(active) VALUES (%s)", tuple(data.values()))
            db_connection.commit()
        else:
            db_object.execute(f"SELECT active FROM entity")
            active_old = db_object.fetchone()
            new_active = ''.join(active_old) + ', ' + data['new']
            db_object.execute(f"UPDATE entity SET active = (%s)", [new_active])
            db_connection.commit()

    await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.activeMenu)


@dp.callback_query_handler(text='btn_active_view')
async def active_view(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    db_object.execute(f"SELECT active FROM entity")

    result = db_object.fetchone()

    if not result:
        await bot.send_message(message.from_user.id, 'У вас нет активов', reply_markup=nav.activeMenu)
    else:
        new_active = 'Ваши активы: ' + ''.join(result)
        await bot.send_message(message.from_user.id, new_active, reply_markup=nav.activeMenu)


########## калькулятор ############
bank_id = None
bank_flag = None


@dp.callback_query_handler(text='btn_calculator')
async def calculator(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.calculatorMenu)


@dp.callback_query_handler(text='btn_condition')
async def condition(message: types.Message):
    global bank_flag
    bank_flag = False
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)


@dp.callback_query_handler(text='btn_sber')
async def sber(message: types.Message):
    global bank, bank_id
    bank = sber
    bank_id = 1
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите роль', reply_markup=nav.roleBankMenu)


@dp.callback_query_handler(text='btn_tinkoff')
async def tinkoff(message: types.Message):
    global bank, bank_id
    bank = tinkoff
    bank_id = 2
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите роль', reply_markup=nav.roleBankMenu)


@dp.callback_query_handler(text='btn_sovcom')
async def sovcom(message: types.Message):
    global bank, bank_id
    bank = sovcom
    bank_id = 3
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите роль', reply_markup=nav.roleBankMenu)


@dp.callback_query_handler(text='btn_bank_back')
async def bank_back(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.bankMenu)


calculFlag = None


@dp.callback_query_handler(text='btn_bank_individual')
async def bank_individual(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите вид кредитования', reply_markup=nav.individualCreditMenu)


def bank_individual_type():
    db_object.execute(f"SELECT to_char (type_of_lending_id,'9999') FROM bank WHERE id = {bank_id}")
    type_of_lending_id = db_object.fetchone()
    type_of = ''.join(type_of_lending_id)
    db_object.execute(f"SELECT to_char (credit_individual_id,'9999') FROM type_of_lending WHERE id = {type_of}")
    credit_individual_id = db_object.fetchone()
    credit_individual = ''.join(credit_individual_id)
    return credit_individual


def bank_individual_type_calcul():
    db_object.execute(f"SELECT to_char (type_of_lending_id,'9999') FROM storage WHERE id = {bank_id}")
    type_of_lending_id = db_object.fetchone()
    db_object.execute(f"SELECT to_char (interest_rate_id,'9999') FROM storage WHERE id = {bank_id}")
    interest_rate_id = db_object.fetchone()
    type_of = ''.join(type_of_lending_id)
    interest_rate = ''.join(interest_rate_id)
    global calculFlag
    calculFlag = False
    db_object.execute(f"SELECT to_char (credit_individual_id,'9999') FROM type_of_lending WHERE id = {type_of}")
    credit_individual_id = db_object.fetchone()
    db_object.execute(f"SELECT to_char (rate,'9999') FROM interest_rate WHERE id = {interest_rate}")
    rateN = db_object.fetchone()
    rate = ''.join(rateN)
    credit_individual = ''.join(credit_individual_id)
    return credit_individual, rate


@dp.callback_query_handler(text='btn_consumer_credit')
async def consumer_credit(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_individual_type()
        db_object.execute(f"SELECT consumer_credit FROM credit_individual WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.individualCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.individualCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMSalaryCredit.salary)
async def process_salary_credit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['salary'] = message.text
    await FSMSalaryCredit.next()
    await bot.send_message(message.from_user.id, 'Введите срок кредитования в месяцах')


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMSalaryCredit.age)
async def process_salary_credit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
        res, rate = bank_individual_type_calcul()
        salaryCredit = int(data['salary']) * int(rate) / 100 * int(data['age']) / 12
        salaryAll = salaryCredit + int(data['salary'])
        rateMonth = int(rate)/12
        salaryMonth = (rateMonth*(1+rateMonth)**int(data['age']))/((1+rateMonth)**int(data['age'])-1)
        salary = int(data['salary'])
        age = int(data['age'])
        textSalary = 'Сумма кредита составит: ' + str(salaryAll) + ', а переплата: ' + str(salaryCredit) + '. Ежемесячный платеж составит: ' + str(salaryMonth)

    db_object.execute(f"SELECT term FROM calculate")
    result = db_object.fetchone()
    db_object.execute(f"INSERT INTO calculate(sum) VALUES (%s)", [salary])
    db_object.execute(f"UPDATE calculate SET term = (%s)", [age])
    db_object.execute(f"UPDATE calculate SET storage_id = (%s)", [bank_id])
    db_connection.commit()

    await state.finish()
    await bot.send_message(message.from_user.id, textSalary, reply_markup=nav.sendMenu)


@dp.callback_query_handler(text='btn_send')
async def send(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    db_object.execute(f"SELECT to_char (id,'9999') FROM user_all")
    result = db_object.fetchone()
    res = ''.join(result)

    db_object.execute(f"SELECT to_char (id,'9999') FROM calculate")
    result = db_object.fetchone()
    resul = ''.join(result)
    db_object.execute(f"INSERT INTO form(user_id) VALUES (%s)", [res])
    db_object.execute(f"UPDATE form SET calculate_id = (%s)", [resul])
    db_connection.commit()

    await bot.send_message(message.from_user.id, 'Ваши данные скоро будут отправлены', reply_markup=nav.startMenu)


@dp.callback_query_handler(text='btn_mortgage')
async def mortgage(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_individual_type()
        db_object.execute(f"SELECT mortgage FROM credit_individual WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.individualCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.individualCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_car_loan')
async def car_loan(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_individual_type()
        db_object.execute(f"SELECT car_loan FROM credit_individual WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.individualCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.individualCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_credit_cart')
async def credit_cart(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_individual_type()
        db_object.execute(f"SELECT credit_card FROM credit_individual WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.individualCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.individualCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_social_credit')
async def social_credit(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_individual_type()
        db_object.execute(f"SELECT social_credit FROM credit_individual WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.individualCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.individualCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


############# юр лица ###############


@dp.callback_query_handler(text='btn_bank_entity')
async def bank_entity(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите вид кредитования', reply_markup=nav.entityCreditMenu)


def bank_entity_type():
    db_object.execute(f"SELECT to_char (type_of_lending_id,'9999') FROM bank WHERE id = {bank_id}")
    type_of_lending_id = db_object.fetchone()
    type_of = ''.join(type_of_lending_id)
    db_object.execute(f"SELECT to_char (credit_entity_id,'9999') FROM type_of_lending WHERE id = {type_of}")
    credit_individual_id = db_object.fetchone()
    credit_individual = ''.join(credit_individual_id)
    return credit_individual


def bank_entity_type_calcul():
    db_object.execute(f"SELECT to_char (type_of_lending_id,'9999') FROM storage WHERE id = {bank_id}")
    type_of_lending_id = db_object.fetchone()
    db_object.execute(f"SELECT to_char (interest_rate_id,'9999') FROM storage WHERE id = {bank_id}")
    interest_rate_id = db_object.fetchone()
    type_of = ''.join(type_of_lending_id)
    interest_rate = ''.join(interest_rate_id)
    global calculFlag
    calculFlag = False
    db_object.execute(f"SELECT to_char (credit_entity_id,'9999') FROM type_of_lending WHERE id = {type_of}")
    credit_individual_id = db_object.fetchone()
    db_object.execute(f"SELECT to_char (rate,'9999') FROM interest_rate WHERE id = {interest_rate}")
    rateN = db_object.fetchone()
    rate = ''.join(rateN)
    credit_individual = ''.join(credit_individual_id)
    return credit_individual, rate


@dp.callback_query_handler(text='btn_single_loan')
async def single_loan(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_entity_type()
        db_object.execute(f"SELECT single_loan FROM credit_entity WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.entityCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.entityCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_credit_line')
async def credit_line(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_entity_type()
        db_object.execute(f"SELECT credit_line FROM credit_entity WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.entityCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.entityCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_overdraft')
async def overdraft(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_entity_type()
        db_object.execute(f"SELECT overdraft FROM credit_entity WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.entityCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.entityCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_investment_loan')
async def investment_loan(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_entity_type()
        db_object.execute(f"SELECT investment_loan FROM credit_entity WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.entityCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.entityCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_commercial_mortgage')
async def commercial_mortgage(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_entity_type()
        db_object.execute(f"SELECT commercial_mortgage FROM credit_entity WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.entityCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.entityCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


@dp.callback_query_handler(text='btn_leasing')
async def leasing(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if bank == None:
        await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)
    else:
        res = bank_entity_type()
        db_object.execute(f"SELECT leasing FROM credit_entity WHERE id = {res}")
        result = db_object.fetchone()
        if not bank_flag:
            if not result:
                await bot.send_message(message.from_user.id, 'У банка нет такого условия',
                                       reply_markup=nav.entityCreditMenu)
            else:
                res = ''.join(result)
                await bot.send_message(message.from_user.id, res, reply_markup=nav.entityCreditMenu)
        else:
            await bot.send_message(message.from_user.id, 'Введите сумму кредита')
            await FSMSalaryCredit.salary.set()


################ посчитать################

@dp.callback_query_handler(text='btn_calcul')
async def calcul(message: types.Message):
    global bank_flag
    bank_flag = True
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите банк', reply_markup=nav.bankMenu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
