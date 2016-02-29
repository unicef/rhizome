import React from 'react'

import AdminApp from '04-pages/AdminApp'

React.render(React.createElement(require('02-molecules/DashboardNav')), document.getElementById('dashboards-nav'))

export default {
  Explorer: function (el) {
    React.render(React.createElement(require('04-pages/Explorer')), el)
  },
  EntryForm: function (el) {
    React.render(React.createElement(require('04-pages/EntryForm')), el)
  },
  SourceData: function (el) {
    React.render(React.createElement(require('04-pages/SourceData')), el)
  },
  UserAccount: function (el, userId) {
    React.render(React.createElement(require('04-pages/UserAccount'), {userId: userId}), el)
  },
  Dashboards: function (el) {
    React.render(React.createElement(require('04-pages/DashboardsPage')), el)
  },
  Dashboard: function (el) {
    React.render(React.createElement(require('04-pages/BuiltinDashboardPage')), el)
  },
  DashboardBuilder: function (el, dashboard_id) {
    React.render(React.createElement(require('04-pages/DashboardBuilder'), { dashboard_id: dashboard_id }), el)
  },
  Charts: function (el) {
    React.render(React.createElement(require('04-pages/ChartsPage')), el)
  },
  Chart: function (el, chart_id) {
    React.render(React.createElement(require('04-pages/ChartPage'), { chart_id: chart_id }), el)
  },
  ChartBuilder: function (el, chart_id) {
    React.render(React.createElement(require('04-pages/ChartWizard'), { chart_id: chart_id }), el)
  },
  HomepageCharts: function (el) {
    React.render(React.createElement(require('04-pages/HomepageChartsView')), el)
  },
  CampaignsPage: function (el, campaignId) {
    React.render(React.createElement(require('04-pages/CampaignsPage'), {campaignId: campaignId}), el)
  },
  UFAdmin: function (el) {
    AdminApp.render(document.getElementById('main'))
  }
}
