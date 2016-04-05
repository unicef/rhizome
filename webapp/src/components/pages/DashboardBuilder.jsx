import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux/src'

// import TitleInput from 'components/molecules/TitleInput'

import LayoutOptions from 'components/molecules/LayoutOptions'
import LayoutDefaultSettings from 'components/organisms/dashboard/builtin/layout-options'
import CustomDashboard from 'components/organisms/dashboard/CustomDashboard'
import DataExplorer from 'components/pages/DataExplorer'

import DashboardBuilderActions from 'actions/DashboardBuilderActions'
import DashboardActions from 'actions/DashboardActions'
import DataActions from 'actions/DataActions'
import GeoActions from 'actions/GeoActions'

import DashboardBuilderStore from 'stores/DashboardBuilderStore'
import DashboardStoreOld from 'stores/DashboardStoreOld'
import DataStore from 'stores/DataStore'

window.perf = React.addons.Perf

export default React.createClass({
  propTypes: {
    dashboard_id: React.PropTypes.number
  },

  mixins: [
    Reflux.connect(DashboardBuilderStore, 'store'),
    Reflux.connect(DataStore, 'dataStore'),
    Reflux.connect(DashboardStoreOld, 'dashboardStore'),
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
    DashboardBuilderActions.initialize(this.props.dashboard_id)
    this.listenTo(DashboardStoreOld, this._onDataLoaded)
    this.listenTo(DashboardStoreOld, this._onDashboardChange)
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
      DataActions.fetchForDashboard(this.state.store.dashboard)
    }
    this.setState({chartBuilderindex: null, chartBuilderActive: false})
  },

  _onDataLoaded () {
    if (this.props.dashboard_id && this.state.store && this.state.dashboardStore && this.state.store.loaded && this.state.dashboardStore.loaded && !this.state.dashboardStore.dashboard) {
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
      let q = DashboardStoreOld.getQueries()
      if (_.isEmpty(q)) {
        DataActions.clear()
      } else {
        if (state.dashboard.builtin) {
          DataActions.fetch(this.state.dashboardStore.campaign, this.state.dashboardStore.location, q)
        } else {
          DataActions.fetchForDashboard(this.state.store.dashboard)
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
      return (
        <form className='inline no-print dashboard-builder-container' onSubmit={this._handleSubmit}>
          <h1>Create a New Custom Dashboard</h1>
          <div className='cd-title small-12'>Dashboard Title</div>
          <input type='text'
            className='description small-12'
            value={this.state.title}
            onChange={this._updateNewTitle}
            autoFocus />
          <div className='cd-title float-none'>Choose a Layout</div>
          <LayoutOptions values={LayoutDefaultSettings.values}
            value={this.state.store.layout}
            onChange={DashboardBuilderActions.changeLayout} />
          <a href='#'
            className={'create-dashboard cd-button float-right ' + (this.state.title.length ? '' : 'disabled')}
            onClick={DashboardBuilderActions.addDashboard}>Next</a>
        </form>
      )
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
      return (<DataExplorer dashboard_id={this.props.dashboard_id}
                           chartDef={chartDef}
                           save={this.saveChart}
                           cancel={this.cancelEditChart}/>)
    } else {
      return dashboardBuilderContainer
    }
  }
})
