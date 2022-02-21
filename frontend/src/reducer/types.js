import createType from "../utils/redux-type-creator";

export const chatTypes = createType(
    'CHAT_START',
    'CHAT_SUCCESS',
    'USER_FAILURE'
)