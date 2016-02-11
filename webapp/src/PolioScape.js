import React from 'react'

import DashboardNav from 'component/DashboardNav.jsx'
import DashboardList from 'view/dashboard-list/DashboardList.jsx'
import AdminApp from './ufadmin'
import CampaignsPage from './ufadmin/CampaignsPage.js'
import HomepageChartsView from 'view/HomepageChartsView.jsx'

React.render(
  React.createElement(DashboardNav),
  document.getElementById('dashboards-nav')
)

export default {
  Explorer: function (el) {
    React.render(React.createElement(require('04-pages/Explorer.jsx')), el)
  },
  Dashboard: function (el) {
    React.render(React.createElement(require('view/Dashboard.jsx')), el)
  },
  DataEntry: function (el) {
    React.render(React.createElement(require('view/entry-form/EntryForm.jsx')), el)
  },
  SourceData: function (el) {
    var SourceData = require('04-pages/SourceData.jsx')
    React.render(React.createElement(SourceData), el)
  },
  UserAccount: function (el, userId) {
    let UserAccount = require('view/user-account/UserAccount.jsx')
    React.render(React.createElement(UserAccount, {userId: userId}), el)
  },
  DashboardList: function (el) {
    React.render(React.createElement(DashboardList), el)
  },
  HomepageCharts: function (el) {
    React.render(React.createElement(HomepageChartsView), el)
  },
  DashboardBuilder: function (el, dashboardId) {
    var DashboardBuilder = require('04-pages/DashboardBuilder.jsx')
    React.render(React.createElement(DashboardBuilder, { dashboardId: dashboardId }), el)
  },
  UFAdmin: function (el) {
    AdminApp.render(document.getElementById('main'))
  },
  CampaignsPage: function (el, campaignId) {
    if (campaignId) {
      React.render(React.createElement(CampaignsPage, {campaignId: campaignId}), el)
    } else {
      React.render(React.createElement(CampaignsPage), el)
    }
  }
}
