import _ from 'lodash'
import uuid from 'uuid'
import Reflux from 'reflux'

import DashboardChartsStore from 'stores/DashboardChartsStore'

import DashboardActions from 'actions/DashboardActions'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'

class Row {
  constructor () {
    this.layout = null
    this.charts = []
  }
}

const DashboardPageStore = Reflux.createStore({

  listenables: DashboardPageActions,

  dashboard: {
    title: '',
    editMode: false,
    chart_uuids: [],
    rows: []
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
    this.dashboard.rows.forEach(row => {
      row.charts.forEach(chart_uuid => DashboardChartsActions.exitEditMode(chart_uuid))
    })
    this.trigger(this.dashboard)
  },

  onSetDashboardTitle: function (title) {
    this.dashboard.title = title
    this.trigger(this.dashboard)
  },

  onAddRow: function () {
    const row = new Row()
    this.dashboard.rows.push(row)
    this.trigger(this.dashboard)
  },

  onSelectRowLayout: function (layout) {
    console.info('')
    console.info('------------------------------------------------------------')
    console.info('DashboardPageStore - onSelectRowLayout')
    const row_index = this.dashboard.rows.length - 1
    this.dashboard.rows[row_index].layout = layout
    this._addChartToRow(row_index)
    if (layout === 2) {
      this._addChartToRow(row_index)
    } else if (layout === 3 || layout === 4) {
      this._addChartToRow(row_index)
      this._addChartToRow(row_index)
    }
    console.log('this.dashboard.rows', this.dashboard.rows)
    this.trigger(this.dashboard)
  },

  _addChartToRow: function (row_index) { console.info('DashboardPageStore - _addChartToRow')
    const chart_uuid = uuid.v4()
    this.dashboard.rows[row_index].charts.push(chart_uuid)
    DashboardChartsActions.addChart(chart_uuid)
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
    this.dashboard.chart_uuids = response.charts.map(chart => chart.uuid)
    this.trigger(this.dashboard)
  },
  onFetchDashboardFailed: function (error) {
    this.setState({ error: error })
  }
})

export default DashboardPageStore
