import {chatTypes} from '../types'

export const chatActionStart = (query)=>({
    type: chatTypes.CHAT_START,
    payload: query
})

export const chatActionSuccess = (res)=>({
    type: chatTypes.CHAT_SUCCESS,
    payload: res
})

export const chatActionFailure = (error)=>({
    type: chatTypes.USER_FAILURE,
    payload: error
})