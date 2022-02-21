import { chatTypes } from "../types";

const initialState = {
    query: [],
    res: [],
    error: ''
}

const chatReducer = (state=initialState, action)=>{

    switch (action.type) {

        case chatTypes.CHAT_START:
            return {
                ...state,
                query: [...state.query, action.payload]
            }

        case chatTypes.CHAT_SUCCESS:
            return {
                ...state,
                query: [...state.query, action.payload],
                error: null
            }
            
        case chatTypes.USER_FAILURE:
            return {
                ...state,
                error: action.payload
            }
    
        default:
            return state
    }
}


export default chatReducer