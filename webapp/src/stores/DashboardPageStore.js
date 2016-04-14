import _ from 'lodash'
import Reflux from 'reflux'

import DashboardChartsStore from 'stores/DashboardChartsStore'

import DashboardActions from 'actions/DashboardActions'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'

const DashboardPageStore = Reflux.createStore({

  listenables: DashboardPageActions,

  dashboard: {
    title: '',
    editMode: false
  },

  charts: {},

  init () {
    this.listenTo(DashboardChartsStore, charts => this.charts = charts)
    this.listenTo(DashboardActions.postDashboard.completed, () => {
      this.dashboard.saving = false
      this.dashboard.editMode = false
      this.trigger(this.dashboard)
    })
  },

  getInitialState: function () {
    return this.dashboard
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //

  onToggleEditMode: function () {
    this.dashboard.editMode = !this.dashboard.editMode
    this.trigger(this.dashboard)
  },

  onSetDashboardTitle: function (title) {
    this.dashboard.title = title
    this.trigger(this.dashboard)
  },

  onSaveDashboard: function (dashboard_id = null) {
    if (!this.dashboard.title || this.dashboard.title === 'Untitled Dashboard') {
      return window.alert('Please add a Title to your dashboard')
    }
    let allChartsSaved = true
    _.toArray(this.charts).forEach(chart => {
      if (!chart.title || chart.title === 'Untitled Chart') {
        allChartsSaved = false
        return
      }
      DashboardChartsActions.saveChart(chart.uuid)
    })
    if (!allChartsSaved) {
      return window.alert('Please title all of your charts')
    }
    this.dashboard.saving = true
    this.trigger(this.dashboard)
    const query = {
      id: dashboard_id,
      title: this.dashboard.title,
      chart_uuids: _.toArray(this.charts).map(chart => chart.uuid)
    }
    DashboardActions.postDashboard(query)
  },

  // =========================================================================== //
  //                               API CALL HANDLERS                             //
  // =========================================================================== //
  // =============================  Fetch Dashboard  =========================== //
  onFetchDashboard: function (uuid) {
    this.trigger(this.dashboard)
  },
  onFetchDashboardCompleted: function (response) {
    this.dashboard.title = response.title
    response.charts.forEach(chart => DashboardChartsActions.fetchChart.completed(chart))
    this.trigger(this.dashboard)
  },
  onFetchDashboardFailed: function (error) {
    this.setState({ error: error })
  }
})

export default DashboardPageStore
