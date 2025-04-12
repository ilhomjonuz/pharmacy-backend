from aiogram.fsm.state import StatesGroup, State


class TypeAddStates(StatesGroup):
    name_uz = State()
    name_ru = State()
    name_en = State()


class CategoryAddStates(StatesGroup):
    name_uz = State()
    name_ru = State()
    name_en = State()


class PartnersAddStates(StatesGroup):
    image = State()


class DoctorsAddStates(StatesGroup):
    direction_uz = State()
    direction_ru = State()
    direction_en = State()
    fullname = State()
    direction = State()
    call = State()
    body_uz = State()
    body_ru = State()
    body_en = State()
    # picture = State()
    advices = State()
    published = State()
    picture = State()


class PillsAddStates(StatesGroup):
    category_choose = State()
    name_uz = State()
    name_ru = State()
    name_en = State()
    information_dori_uz = State()
    information_dori_ru = State()
    information_dori_en = State()
    narxi = State()
    tarkibi_uz = State()
    tarkibi_ru = State()
    tarkibi_en = State()
    dori_turi = State()
    yaroqlilik_muddati = State()
    video_manzili = State()
    rasmi = State()
    chegirma_narxi = State()
    # saytda_korinishi = State()
    ommabopmi = State()
    reyting = State()


class IzohlarAddStates(StatesGroup):
    avtor = State()
    body = State()

