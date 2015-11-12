'use strict'

var React = require('react')
var Vue = require('vue')

var LandingPage = require('view/LandingPage.jsx')
var DashboardNav = require('component/DashboardNav.jsx')
var DashboardList = require('view/dashboard-list/DashboardList.jsx')
var AdminApp = require('./ufadmin')
var CampaignsPage = require('./ufadmin/CampaignsPage.js')
var GroupForm = require('view/group-form/GroupForm.jsx')
var HomepageChartsView = require('view/HomepageChartsView.jsx')

Vue.config.debug = true

Vue.component('vue-dropdown', require('./component/dropdown'))
Vue.component('vue-table', require('./component/table'))
Vue.component('vue-table-editable', require('./component/table-editable'))
Vue.component('vue-pagination', require('./component/pagination'))
Vue.component('vue-tooltip', require('./component/vue-tooltip'))
Vue.component('vue-menu', require('./component/vue-menu'))

Vue.filter('num', require('./filter/num'))

Vue.partial('tooltip-stacked-bar', require('./partial/tooltip-stacked-bar.html'))
Vue.partial('tooltip-heatmap', require('./partial/tooltip-heatmap.html'))
Vue.partial('tooltip-indicator', require('./partial/tooltip-indicator.html'))

React.render(
  React.createElement(DashboardNav),
  document.getElementById('dashboards-nav')
)

module.exports = {
  Explorer: function (el) {
    let vue = new Vue({
      el: el,
      components: { 'uf-explorer': require('./view/explorer') }
    })
    return vue
  },
  Dashboard: function (el) {
    React.render(React.createElement(require('view/Dashboard.jsx')), el)
  },
  DataEntry: function (el) {
    let vue = new Vue({
      el: el,
      components: { 'uf-entry-form': require('./view/entry-form') }
    })
    return vue
  },
  UserAccount: function (el, user_id) {
    let vue = new Vue({
      el: el,
      components: { 'uf-user-account': require('./view/user-account') },
      data: {'user_id': user_id}
    })
    return vue
  },
  LandingPage: function (el) {
    React.render(React.createElement(LandingPage), el)
  },
  DashboardList: function (el) {
    React.render(React.createElement(DashboardList), el)
  },
  HomepageCharts: function (el) {
    React.render(React.createElement(HomepageChartsView), el)
  },
  DashboardBuilder: function (el, dashboardId) {
    var DashboardBuilder = require('view/dashboard-builder/DashboardBuilder.jsx')
    React.render(React.createElement(DashboardBuilder, { dashboardId: dashboardId }), el)
  },
  ChartBuilder: function (el, dashboard_id) {
    var ChartBuilder = require('view/chart-builder/ChartBuilder.jsx')
    React.render(React.createElement(ChartBuilder, { dashboard_id: dashboard_id }), el)
  },
  UFAdmin: function (el) {
    AdminApp.render(document.getElementById('main'))
  },
  CampaignsPage: function (id_start_date, id_end_date) {
    CampaignsPage.render(id_start_date, id_end_date)
  },
  GroupForm: function (el, group_id) {
    React.render(React.createElement(GroupForm, { group_id: group_id }), el)
  }
}
