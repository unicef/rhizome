import React from 'react'
import ReactDOM from 'react-dom'
import { createStore, applyMiddleware, compose } from 'redux'
import { Provider } from 'react-redux'
import { Router, browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'
import createSagaMiddleware from 'redux-saga'
import NProgress from 'react-nprogress'
import Routes from 'Routes'
import rootReducer from 'reducers/_index'
import {rootSaga} from 'sagas'

const sagaMiddleware = createSagaMiddleware()
const middleware = applyMiddleware(sagaMiddleware)
const chromeDevToolExtension = window.devToolsExtension ? window.devToolsExtension() : f => f
const createStoreWithMiddleware = compose(middleware, chromeDevToolExtension)(createStore)
const store = createStoreWithMiddleware(rootReducer)
const history = syncHistoryWithStore(browserHistory, store)

let showProgressBar = () => NProgress.done()

sagaMiddleware.run(rootSaga)

ReactDOM.render((
  <Provider store={store}>
    <Router history={history} onUpdate={showProgressBar} routes={Routes} />
  </Provider>
), document.getElementById('root'))
