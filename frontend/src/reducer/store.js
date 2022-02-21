import {createStore, applyMiddleware} from 'redux'
import logger from 'redux-logger'
import rootReducer from './rootReducer'
import  createSagaMiddleware from 'redux-saga'
import sagaRoot from './redux-saga-root'

const sageMiddleware = createSagaMiddleware()
const middlewares = [sageMiddleware, logger]
const store = createStore(rootReducer, applyMiddleware(...middlewares))
sageMiddleware.run(sagaRoot)

export default store