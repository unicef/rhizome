require('utilities/polyfill.js')

import React from 'react'
import Reflux from 'reflux'
import RefluxPromise from 'reflux-promise'
import AdminApp from 'components/pages/AdminApp'
// import SourceDataApp from 'components/pages/SourceDataApp'

Reflux.use(RefluxPromise(window.Promise))

React.render(React.createElement(require('components/atoms/nav/DashboardNav')), document.getElementById('dashboards-nav'))

const Rhizome = window.Rhizome = {
  DataEntry: function (el) {
    React.render(React.createElement(require('components/pages/DataEntry')), el)
  },
  UserAccount: function (el, userId) {
    React.render(React.createElement(require('components/pages/UserAccount'), {userId: userId}), el)
  },
  Dashboards: function (el) {
    React.render(React.createElement(require('components/pages/DashboardsPage')), el)
  },
  Dashboard: function (el, dashboard_id) {
    React.render(React.createElement(require('components/pages/DashboardPage'), { dashboard_id: dashboard_id }), el)
  },
  Charts: function (el) {
    React.render(React.createElement(require('components/pages/ChartsPage')), el)
  },
  ChartPage: function (el, chart_id) {
    React.render(React.createElement(require('components/pages/ChartPage'), { chart_id: chart_id }), el)
  },
  CampaignsPage: function (el, campaignId) {
    React.render(React.createElement(require('components/pages/CampaignsPage'), {campaignId: campaignId}), el)
  },
  SourceData: function (el) {
    React.render(React.createElement(require('components/pages/SourceData')), el)
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
