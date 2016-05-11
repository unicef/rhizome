// require('./utilities/polyfill.js')

import React from 'react'
import Reflux from 'reflux'
import RefluxPromise from 'reflux-promise'
import AdminApp from 'containers/AdminApp'
// import SourceDataApp from 'containers/SourceDataApp'

Reflux.use(RefluxPromise(window.Promise))

React.render(React.createElement(require('components/nav/DashboardNav')), document.getElementById('dashboards-nav'))

const Rhizome = window.Rhizome = {
  DataEntry: function (el) {
    React.render(React.createElement(require('containers/DataEntryContainer')), el)
  },
  UserAccount: function (el, userId) {
    React.render(React.createElement(require('containers/UserAccount'), {userId: userId}), el)
  },
  Dashboards: function (el) {
    React.render(React.createElement(require('containers/DashboardsContainer')), el)
  },
  Dashboard: function (el, dashboard_id) {
    React.render(React.createElement(require('containers/DashboardContainer'), { dashboard_id: dashboard_id }), el)
  },
  Charts: function (el) {
    React.render(React.createElement(require('containers/ChartsContainer')), el)
  },
  ChartContainer: function (el, chart_id) {
    React.render(React.createElement(require('containers/ChartContainer'), { chart_id: chart_id }), el)
  },
  CampaignsContainer: function (el, campaignId) {
    React.render(React.createElement(require('containers/CampaignsContainer'), {campaignId: campaignId}), el)
  },
  SourceData: function (el) {
    React.render(React.createElement(require('containers/SourceDataContainer')), el)
    // SourceDataApp.render(document.getElementById('main'))
  },
  ManageSystem: function (el) {
    AdminApp.render(document.getElementById('main'))
  }
}

if ('ActiveXObject' in window) {
  var body = document.getElementsByTagName('body')[0]
  body.classList.add('ie')
}

export default Rhizome
