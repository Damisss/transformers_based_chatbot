import {all, call} from 'redux-saga/effects'
import {onUserMessage} from './chat/chat.saga'

function* sagaRoot(){
    yield  all([
        call(onUserMessage)
    ])
}

export default sagaRoot