from aiogram.fsm.state import State, StatesGroup

# Определение состояний FSM
class RegisterState(StatesGroup):
    waiting_for_class = State()
    confirm_class = State()

class ReviewState(StatesGroup):
    waiting_for_text = State()
    waiting_for_photo = State()
    waiting_for_rating = State()
    confirm_review = State()

class AdminAuthState(StatesGroup):
    waiting_for_password = State()

class FilterReviewsState(StatesGroup):
    waiting_for_class = State() 