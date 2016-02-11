import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux/src'
import ChartWizard from '04-pages/ChartWizard.jsx'

import DataActions from 'actions/DataActions'
import DataStore from 'stores/DataStore'

import DashboardBuilderActions from 'actions/DashboardBuilderActions'
import DashboardBuilderStore from 'stores/DashboardBuilderStore'

import DashboardActions from 'actions/DashboardActions'
import DashboardStore from 'stores/DashboardStore'

import GeoActions from 'actions/GeoActions'
// import TitleInput from 'component/TitleInput.jsx'
// import LayoutOptions from 'component/layout-options/LayoutOptions.jsx'
// import LayoutDefaultSettings from '03-organisms/dashboard/builtin/layout-options'
import CustomDashboard from '03-organisms/dashboard/CustomDashboard.jsx'

window.perf = React.addons.Perf

export default React.createClass({
  propTypes: {
    dashboardId: React.PropTypes.number
  },

  mixins: [
    Reflux.connect(DashboardBuilderStore, 'store'),
    Reflux.connect(DataStore, 'dataStore'),
    Reflux.connect(DashboardStore, 'dashboardStore'),
    Reflux.ListenerMixin
  ],

  getInitialState () {
    return {
      chartBuilderActive: false,
      chartBuilderindex: null,
      title: '',
      description: ''
    }
  },

  componentDidMount () {
    DashboardBuilderActions.initialize(this.props.dashboardId)
    this.listenTo(DashboardStore, this._onDataLoaded)
    this.listenTo(DashboardStore, this._onDashboardChange)
  },

  editChart (index) {
    this.setState({chartBuilderindex: index, chartBuilderActive: true})
  },

  cancelEditChart () {
    this.setState({chartBuilderindex: null, chartBuilderActive: false})
  },

  moveForward (index) {
    DashboardBuilderActions.moveForward(index)
  },

  moveBackward (index) {
    DashboardBuilderActions.moveBackward(index)
  },

  deleteChart (index) {
    let chart = _.get(this.state, `store.dashboard.charts[${index}].title`, '')
    if (_.isEmpty(chart)) {
      chart = 'this chart'
    } else {
      chart = `"${chart}"`
    }

    let dashboard = _.get(this.state, 'store.dashboard.title', '')
    if (_.isEmpty(dashboard)) {
      dashboard = 'the dashboard'
    }

    if (window.confirm(`Delete ${chart} from ${dashboard}?`)) {
      // FIXME
      DashboardBuilderActions.removeChart(index)
    }
  },

  _deleteDashboard () {
    if (window.confirm(`Delete dashboard "${this.state.title}"?`)) {
      DashboardBuilderActions.deleteDashboard()
    }
  },

  newChart () {
    this.setState({chartBuilderindex: null, chartBuilderActive: true})
  },

  saveChart (chartDef) {
    if (!_.isNull(this.state.chartBuilderindex)) {
      DashboardBuilderActions.updateChart(chartDef, this.state.chartBuilderindex)
    } else {
      DashboardBuilderActions.addChart(chartDef)
      DataActions.fetchForChart(this.state.store.dashboard)
    }
    this.setState({chartBuilderindex: null, chartBuilderActive: false})
  },

  _onDataLoaded () {
    if (this.props.dashboardId && this.state.store && this.state.dashboardStore && this.state.store.loaded && this.state.dashboardStore.loaded && !this.state.dashboardStore.dashboard) {
      DashboardActions.setDashboard({ dashboard: this.state.store.dashboard })
      this.setState({
        title: this.state.store.dashboard.title,
        description: this.state.store.dashboard.description
      })
    }
  },

  _onDashboardChange (state) {
    let dashboardSet = this.state.dashboardStore.dashboard
    if (dashboardSet) {
      let q = DashboardStore.getQueries()
      if (_.isEmpty(q)) {
        DataActions.clear()
      } else {
        if (state.dashboard.builtin) {
          DataActions.fetch(this.state.dashboardStore.campaign, this.state.dashboardStore.location, q)
        } else {
          DataActions.fetchForChart(this.state.store.dashboard)
        }
      }
      this.state.dashboardStore.hasMap && GeoActions.fetch(this.state.dashboardStore.location)
    }
  },

  _updateTitle (newText) {
    DashboardBuilderActions.updateTitle(newText)
  },

  _updateNewTitle (e) {
    this.setState({title: e.currentTarget.value})
    DashboardBuilderActions.updateTitle(e.currentTarget.value)
  },

  _updateDescription (newText) {
    DashboardBuilderActions.updateDescription(newText)
  },

  _handleSubmit (e) {
    e.preventDefault()
    DashboardBuilderActions.addDashboard()
  },

  render () {
    if (this.state.store.newDashboard) {
      var chartDef = {'indicators': [], 'type': 'LineChart'}
      return (<ChartWizard dashboardId={-1}
                           chartDef={chartDef}
                           save={this.saveChart}
                           cancel={this.cancelEditChart}/>)
    } else if (!(this.state.dashboardStore && this.state.dashboardStore.loaded && this.state.dashboardStore.dashboard) || this.state.dataStore.loading) {
      let style = {fontSize: '2rem', zIndex: 9999}
      return (
        <div style={style} className='overlay'>
          <div>
            <div><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
          </div>
        </div>
      )
    }

    let dashboardDef = this.state.store.dashboard
    let loaded = this.state.dashboardStore.loaded

    let dashboardProps = {
      campaigns: this.state.dashboardStore.campaigns,
      dashboard: dashboardDef,
      data: this.state.dataStore.data,
      loading: !loaded,
      editable: true,
      onAddChart: this.newChart,
      onEditChart: this.editChart,
      onDeleteChart: this.deleteChart,
      onMoveForward: this.moveForward,
      onMoveBackward: this.moveBackward
    }

    let dashboard = React.createElement(CustomDashboard, dashboardProps)

    let addDashboardLinkContainer = (
      <div className='empty-dashboard-add-container'>
        <span className='cd-button new-dashboard-font' onClick={this.newChart}>
          <i className='fa fa-icon fa-fw fa-plus'></i>&ensp;Add New Chart to Dashboard
        </span>
      </div>
    )

    let dashboardBuilderContainer = (
      <div>
        {this.state.store.dashboard.charts.length ? dashboard : addDashboardLinkContainer}
        <div className='cd-footer'>
          <div className='row'>
            <div className='large-2 columns'>
            </div>
            <div className='large-7 columns'>
            </div>
            <div className='large-3 columns'>
            </div>
          </div>
        </div>
      </div>
    )
    if (!this.state.store.loaded) {
      return (<div>loading</div>)
    } else if (this.state.chartBuilderActive) {
      let chartDef = _.isNull(this.state.chartBuilderindex)
        ? null
        : this.state.store.dashboard.charts[this.state.chartBuilderindex]
      return (<ChartWizard dashboardId={this.props.dashboardId}
                           chartDef={chartDef}
                           save={this.saveChart}
                           cancel={this.cancelEditChart}/>)
    } else {
      return dashboardBuilderContainer
    }
  }
})
