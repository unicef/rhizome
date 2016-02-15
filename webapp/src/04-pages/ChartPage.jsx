import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import page from 'page'

import ChartAPI from 'data/requests/ChartAPI'

var ChartPage = React.createClass({

  getInitialState () {
    return {
    }
  },

  componentWillMount () {
    // page('/datapoints/dashboards/:dashboard')
  },

  componentWillUpdate (nextProps, nextState) {

  },

  componentDidMount () {

  },

  render () {
    return (
      <div>
        <h1>Chart View Coming Soon</h1>
      </div>
    )
  }
})

export default ChartPage
