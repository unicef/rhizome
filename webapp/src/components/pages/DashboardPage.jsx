import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import AsyncButton from 'components/atoms/AsyncButton'

import Placeholder from 'components/molecules/Placeholder'
import MultiChart from 'components/organisms/MultiChart'
import TitleInput from 'components/molecules/TitleInput'

import RootStore from 'stores/RootStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardPageStore from 'stores/DashboardPageStore'

import DashboardActions from 'actions/DashboardActions'
import DashboardPageActions from 'actions/DashboardPageActions'

const Dashboard = React.createClass({

  mixins: [
    Reflux.connect(DashboardPageStore, 'dashboard'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    dashboard_id: PropTypes.number
  },

  getInitialState () {
    return {
      titleEditMode: false,
      readOnlyMode: this.props.dashboard_id ? true : false
    }
  },

  componentDidMount () {
    // Wait for initial data to be ready and either fetch the dashboard or load a fresh chart
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index) {
        if (this.props.dashboard_id) {
          DashboardPageActions.fetchDashboard(this.props.dashboard_id)
        } else {
          DashboardPageActions.addChart()
        }
      }
    })
    // If the dashboard is saved for the first time, redirect to the dashboard page
    this.listenTo(DashboardActions.postDashboard.completed, (response) => {
      if (!this.props.dashboard_id) {
        const dashboard_id = response.objects.id
        window.location = window.location.origin + '/dashboards/' + dashboard_id
      }
    })
  },

  shouldComponentUpdate (nextProps, nextState) {
    const charts = _.toArray(nextState.dashboard.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    return !this.missing_data || this.missing_params || this.loading_charts
  },

  _toggleTitleEdit (title) {
    if (_.isString(title)) {
      DashboardPageActions.setDashboardTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  _toggleReadOnlyMode (title) {
    this.setState({readOnlyMode: !this.state.readOnlyMode})
  },

  render () {
    const readOnlyMode = this.state.readOnlyMode
    const dashboard = this.state.dashboard
    const charts = _.toArray(dashboard.charts)
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={dashboard.title} save={this._toggleTitleEdit}/>
      :
      <h1 onClick={this._toggleTitleEdit}>
        <a>{dashboard.title || 'Untitled Dashboard'}</a>
      </h1>

    const chart_components = charts.map(chart => (
        <div className='row'>
          <MultiChart
            chart={chart}
            readOnlyMode={readOnlyMode}
            linkCampaigns={() => DashboardPageActions.toggleCampaignLink(chart.uuid)}
            duplicateChart={DashboardPageActions.duplicateChart}
            selectChart={new_chart => DashboardPageActions.selectChart(new_chart, chart.uuid)}
            toggleSelectTypeMode={() => DashboardPageActions.toggleSelectTypeMode(chart.uuid)}
            toggleEditMode={() => DashboardPageActions.toggleEditMode(chart.uuid)}
            removeChart={DashboardPageActions.removeChart}
            saveChart={() => DashboardPageActions.saveChart(chart.uuid)}
            setDateRange={(key, value) => DashboardPageActions.setDateRange(key, value, chart.uuid)}
            setGroupBy={(grouping) => DashboardPageActions.setGroupBy(grouping, chart.uuid)}
            setPalette={(palette) => DashboardPageActions.setPalette(palette, chart.uuid)}
            setTitle={(title) => DashboardPageActions.setChartTitle(title, chart.uuid)}
            setType={(type) => DashboardPageActions.setType(type, chart.uuid)}
            setIndicators={(indicators) => DashboardPageActions.setIndicators(indicators, chart.uuid)}
            selectIndicator={(id) => DashboardPageActions.selectIndicator(id, chart.uuid)}
            deselectIndicator={(id) => DashboardPageActions.deselectIndicator(id, chart.uuid)}
            reorderIndicator={(indicators) => DashboardPageActions.reorderIndicator(indicators, chart.uuid)}
            clearSelectedIndicators={() => DashboardPageActions.clearSelectedIndicators(chart.uuid)}
            setLocations={(locations) => DashboardPageActions.setLocations(locations, chart.uuid)}
            selectLocation={(id) => DashboardPageActions.selectLocation(id, chart.uuid)}
            deselectLocation={(id) => DashboardPageActions.deselectLocation(id, chart.uuid)}
            clearSelectedLocations={() => DashboardPageActions.clearSelectedLocations(chart.uuid)}
            setCampaigns={(campaigns) => DashboardPageActions.setCampaigns(campaigns, chart.uuid)}
            selectCampaign={(id) => DashboardPageActions.selectCampaign(id, chart.uuid)}
            deselectCampaign={(id) => DashboardPageActions.deselectCampaign(id, chart.uuid)}
          />
        </div>
      )
    )

    const save_dashboard_button = !readOnlyMode ? (
      <AsyncButton
        text='Save Dashboard'
        alt_text='Saving ...'
        isBusy={dashboard.saving}
        onClick={() => DashboardPageActions.saveDashboard(this.props.dashboard_id)}
      />
    ) : null

    const add_chart_button = loading || !readOnlyMode ? (
      <div className='row text-center'>
        <button
          className='button large'
          onClick={DashboardPageActions.addChart}
          style={{marginTop: '1rem'}}>
          Add Chart
        </button>
      </div>
    ) : null

    const loading = !charts.length > 0

    return (
      <section className='dashboard'>
        <header className='row dashboard-header'>
          <div className='medium-6 columns medium-text-left small-text-center'>
            { !readOnlyMode ? title_bar : <h1>{dashboard.title || 'Untitled Dashboard'}</h1> }
          </div>
          <div className='medium-6 columns medium-text-right small-text-center'>
            { save_dashboard_button }
            <button className='button' onClick={this._toggleReadOnlyMode}>
              { readOnlyMode ? 'Edit Dashboard' : 'Exit Edit Mode' }
            </button>
          </div>
        </header>
        { loading ? <Placeholder height={600} /> : chart_components}
        { add_chart_button }
      </section>
    )
  }
})

export default Dashboard
