import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux/src'
import ChartWizard from 'view/chart-wizard/ChartWizard.jsx'

import DataActions from 'actions/DataActions'
import DataStore from 'stores/DataStore'

import DashboardBuilderActions from 'actions/DashboardBuilderActions'
import DashboardBuilderStore from 'stores/DashboardBuilderStore'

import DashboardActions from 'actions/DashboardActions'
import DashboardStore from 'stores/DashboardStore'

import GeoActions from 'actions/GeoActions'
import TitleInput from 'component/TitleInput.jsx'
import LayoutOptions from 'component/layout-options/LayoutOptions.jsx'
import LayoutDefaultSettings from 'dashboard/builtin/layout-options'
import CustomDashboard from 'dashboard/CustomDashboard.jsx'

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

    let showAddChartButton = () => {
      let layout = this.state.store.dashboard.layout
      let numCharts = this.state.store.dashboard.charts.length
      return (
        (layout === 1 && !numCharts) ||
        (layout === 2 && numCharts < 8) ||
        (layout === 3 && numCharts < 3)
      )
    }
    let dashboardBuilderContainer = (
      <div>
        <form className='inline no-print row cd-titlebar'>
          <div className='large-6 columns'> </div>
          <div className='large-6 columns'>
            <div className='row'>
              <div className='large-6 medium-4 small-12 columns'>
                <label className='cd-title-label cd-titlebar-margin'>Dashboard Title</label>
              </div>
              <div className='large-6 medium-8 small-12 columns'>
                <TitleInput className='cd-title-input cd-titlebar-margin'
                            initialText={this.state.title}
                            save={this._updateTitle}/>
              </div>
            </div>
          </div>
        </form>
        {this.state.store.dashboard.charts.length ? dashboard : addDashboardLinkContainer}
        <div className='cd-footer'>
          <div className='row'>
            <div className='large-2 columns'>
              <button className='cd-button'
                      onClick={this.newChart}
                      style={{visibility: (showAddChartButton() ? 'visible' : 'hidden')}}>
                <span> <i className='fa fa-icon fa-fw fa-plus' /> Add Chart </span>
              </button>
            </div>
            <div className='large-7 columns'>
              <div className='row'>
                <div className='large-2 columns'>
                  <label className='description-text'>Description&ensp;:</label>
                </div>
                <div className='large-5 columns'>
                  <TitleInput className='description' initialText={this.state.description}
                              save={this._updateDescription}/>
                </div>
                <div className='large-5 columns'>
                  <div className='description-text'>Changes are saved when you make them.</div>
                </div>
              </div>
            </div>
            <div className='large-3 columns'>
              <button className='cd-button float-right' href='#' onClick={this._deleteDashboard}>
                <i className='fa fa-icon fa-fw fa-trash'/>Delete this dashboard
              </button>
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
