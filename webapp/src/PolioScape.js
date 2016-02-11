import React from 'react'

import AdminApp from '04-pages/AdminApp'

React.render(React.createElement(require('component/DashboardNav')), document.getElementById('dashboards-nav'))

export default {
  Explorer: function (el) {
    React.render(React.createElement(require('04-pages/Explorer')), el)
  },
  Dashboard: function (el) {
    React.render(React.createElement(require('04-pages/Dashboard')), el)
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
  DashboardList: function (el) {
    React.render(React.createElement(require('04-pages/DashboardList')), el)
  },
  HomepageCharts: function (el) {
    React.render(React.createElement(require('04-pages/HomepageChartsView')), el)
  },
  DashboardBuilder: function (el, dashboardId) {
    React.render(React.createElement(require('04-pages/DashboardBuilder'), { dashboardId: dashboardId }), el)
  },
  CampaignsPage: function (el, campaignId) {
    React.render(React.createElement(require('04-pages/CampaignsPage'), {campaignId: campaignId}), el)
  },
  UFAdmin: function (el) {
    AdminApp.render(document.getElementById('main'))
  }
}
