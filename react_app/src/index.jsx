import React from 'react'
import ReactDOM from 'react-dom'
import { createStore, applyMiddleware, compose } from 'redux'
import { Provider } from 'react-redux'
import { Router, browserHistory } from 'react-router'
import { syncHistoryWithStore } from 'react-router-redux'
import ReduxPromise from 'redux-promise'
import NProgress from 'react-nprogress'
import Routes from 'Routes'
import rootReducer from 'reducers/_index'

const chromeDevToolExtension = window.devToolsExtension ? window.devToolsExtension() : f => f
const createStoreWithMiddleware = compose(applyMiddleware(ReduxPromise), chromeDevToolExtension)(createStore)
const store = createStoreWithMiddleware(rootReducer)
const history = syncHistoryWithStore(browserHistory, store)

let showProgressBar = () => NProgress.done()

ReactDOM.render((
  <Provider store={store}>
    <Router history={history} onUpdate={showProgressBar} routes={Routes} />
  </Provider>
), document.getElementById('root'))
