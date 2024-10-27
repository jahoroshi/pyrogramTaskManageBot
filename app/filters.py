from typing import Tuple, Any

from pyrogram import filters

from app.states import state


def state_filter(states: Tuple[Any, Any]):
    async def custom_filter(_, __, message):
        user_id = message.from_user.id
        cur_state = await state.get_state(user_id)
        return cur_state is not None and cur_state in states
    return filters.create(custom_filter)

