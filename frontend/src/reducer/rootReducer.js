import {combineReducers} from 'redux'
import chatReducer from './chat/chat.reducer'

const rootReducer = combineReducers({
    chat: chatReducer
})

export default rootReducer