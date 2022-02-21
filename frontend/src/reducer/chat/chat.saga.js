import {put, takeLatest} from 'redux-saga/effects'
import {chatActionSuccess, chatActionFailure} from './chat.action'
import {chatTypes} from '../types'

function* userMessage({payload}){
    console.log(payload.message)
   try {
        const response = yield fetch('http://localhost:3001/intent-recognition', {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                Accept: 'application/json'
            },
            body: JSON.stringify({
                query: payload.message
            })
        })
        const chat = yield response.json()
        
        if (chat.status_code !== 200){
            throw new Error(JSON.stringify(chat))
        }
            

        yield put(
            chatActionSuccess(chat)
        )
       
   } catch (error) {
    yield put(
        chatActionFailure({error})
    )
   }
}

export function* onUserMessage(){
    yield takeLatest(chatTypes.CHAT_START, userMessage)
}