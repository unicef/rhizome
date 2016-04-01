import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import Placeholder from 'components/molecules/Placeholder'
import MultiChart from 'components/organisms/MultiChart'
import TitleInput from 'components/molecules/TitleInput'

import RootStore from 'stores/RootStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardNewStore from 'stores/DashboardNewStore'

import DashboardNewActions from 'actions/DashboardNewActions'
import ChartActions from 'actions/ChartActions'
import DashboardActions from 'actions/DashboardActions'

const Dashboard = React.createClass({

  mixins: [
    Reflux.connect(DashboardNewStore, 'dashboard'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    dashboard_id: PropTypes.number
  },

  getInitialState () {
    return {
      titleEditMode: false
    }
  },

  componentDidMount () {
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index) {
        if (this.props.dashboard_id) {
          DashboardNewActions.fetchDashboard(this.props.dashboard_id)
        } else {
          DashboardNewActions.addChart()
        }
      }
    })
  },

  shouldComponentUpdate(nextProps, nextState) {
    this.allChartsReady = true
    _.toArray(nextState.dashboard.charts).forEach(chart => {
      const missing_params = _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)
      this.allChartsReady = (chart.data && chart.data.length > 1) || missing_params
    })
    return this.allChartsReady
  },

  _toggleTitleEdit (title) {
    if (_.isString(title)) {
      DashboardNewActions.setDashboardTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  saveDashboard () {
    const dashboard = this.state.dashboard
    console.info('- Dashboard.saveChart', dashboard.title)
    if (!dashboard.title || dashboard.title === 'Untitled Dashboard') {
      return window.alert('Please add a Title to your dashboard')
    }
    let allChartsSaved = true
    _.toArray(dashboard.charts).forEach(chart => {
      if (!chart.title || chart.title === 'Untitled Chart') {
       return allChartsSaved = false
      }
      this.saveChart(chart)
    })
    if (!allChartsSaved) {
      return window.alert('Please title all of your charts')
    }

    const query = {
      id: this.props.dashboard_id || null,
      title: dashboard.title,
      chart_uuids: _.toArray(dashboard.charts).map(chart => chart.uuid)
    }
    console.log('query', query)
    DashboardActions.postDashboard(query)
  },

  saveChart (chart) {
    console.info('- Dashboard.saveChart')
    if (!chart.title || chart.title === 'Untitled Chart') {
      return window.alert('Please add a Title to your chart')
    }
    ChartActions.postChart({
      id: chart.id,
      title: chart.title,
      uuid: chart.uuid,
      chart_json: JSON.stringify({
        type: chart.type,
        start_date: chart.start_date,
        end_date: chart.end_date,
        campaign_ids: chart.selected_campaigns.map(campaign => campaign.id),
        location_ids: chart.selected_locations.map(location => location.id),
        indicator_ids: chart.selected_indicators.map(indicator => indicator.id)
      })
    })
  },

  render () {
    const dashboard = this.state.dashboard
    const charts = _.toArray(dashboard.charts)
    console.info('Dashboard.RENDER ========================================== Charts:', charts)
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={dashboard.title} save={this._toggleTitleEdit}/>
      :
      <h1 onClick={this._toggleTitleEdit} className='left'>
        <a>
          {dashboard.title || 'Untitled Dashboard'}
        </a>
      </h1>

    const chart_components = charts.map(chart => {
      return (
        <div className='row'>
          <MultiChart
            chart={chart}
            linkCampaigns={() => DashboardNewActions.toggleCampaignLink(chart.uuid)}
            duplicateChart={DashboardNewActions.duplicateChart}
            selectChart={new_chart => DashboardNewActions.selectChart(new_chart, chart.uuid)}
            toggleSelectTypeMode={() => DashboardNewActions.toggleSelectTypeMode(chart.uuid)}
            removeChart={DashboardNewActions.removeChart}
            saveChart={this.saveChart}
            setDateRange={(key, value) => DashboardNewActions.setDateRange(key, value, chart.uuid)}
            setPalette={(palette) => DashboardNewActions.setPalette(palette, chart.uuid)}
            setTitle={(title) => DashboardNewActions.setChartTitle(title, chart.uuid)}
            setType={(type) => DashboardNewActions.setType(type, chart.uuid)}
            setIndicators={(indicators) => DashboardNewActions.setIndicators(indicators, chart.uuid)}
            selectIndicator={(id) => DashboardNewActions.selectIndicator(id, chart.uuid)}
            deselectIndicator={(id) => DashboardNewActions.deselectIndicator(id, chart.uuid)}
            reorderIndicator={(indicators) => DashboardNewActions.reorderIndicator(indicators, chart.uuid)}
            clearSelectedIndicators={() => DashboardNewActions.clearSelectedIndicators(chart.uuid)}
            setLocations={(locations) => DashboardNewActions.setLocations(locations, chart.uuid)}
            selectLocation={(id) => DashboardNewActions.selectLocation(id, chart.uuid)}
            deselectLocation={(id) => DashboardNewActions.deselectLocation(id, chart.uuid)}
            clearSelectedLocations={() => DashboardNewActions.clearSelectedLocations(chart.uuid)}
            setCampaigns={(campaigns) => DashboardNewActions.setCampaigns(campaigns, chart.uuid)}
            selectCampaign={(id) => DashboardNewActions.selectCampaign(id, chart.uuid)}
            deselectCampaign={(id) => DashboardNewActions.deselectCampaign(id, chart.uuid)}
          />
        </div>
      )
    })
    const loading = !charts.length > 0 || !this.allChartsReady
    return (
      <section className='dashboard'>
        <header className='row dashboard-header'>
          <div className='medium-6 columns'>
            { title_bar }
          </div>
          <div className='medium-6 columns'>
            <button className='button right' onClick={this.saveDashboard}>Save Dashboard</button>
          </div>
        </header>
        { loading ? <Placeholder height={600} /> : chart_components}
        { loading ? null : (
            <div className='row text-center'>
              <button
                className='button large'
                onClick={DashboardNewActions.addChart}
                style={{marginTop: '1rem'}}>
                Add Chart
              </button>
            </div>
          )
        }
      </section>
    )
  }
})

export default Dashboard
