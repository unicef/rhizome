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
import DashboardPageStore from 'stores/DashboardPageStore'

import DashboardPageActions from 'actions/DashboardPageActions'
import ChartActions from 'actions/ChartActions'
import DashboardActions from 'actions/DashboardActions'

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
      titleEditMode: false
    }
  },

  componentDidMount () {
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
  },

  shouldComponentUpdate(nextProps, nextState) {
    const charts = _.toArray(nextState.dashboard.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    // console.log('missing_params', this.missing_params)
    // console.log('missing_data', this.missing_data)
    // console.log('loading_charts', this.loading_charts)
    return !this.missing_data || this.missing_params || this.loading_charts
  },

  _toggleTitleEdit (title) {
    if (_.isString(title)) {
      DashboardPageActions.setDashboardTitle(title)
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

  renderChartRow (row) {
    return (
      row.map(chart =>
        <div className={(row.length === 2 ? 'medium-12' : 'medium-12') + ' columns'}>
          <MultiChart
            chart={chart}
            linkCampaigns={() => DashboardPageActions.toggleCampaignLink(chart.uuid)}
            duplicateChart={DashboardPageActions.duplicateChart}
            selectChart={new_chart => DashboardPageActions.selectChart(new_chart, chart.uuid)}
            toggleSelectTypeMode={() => DashboardPageActions.toggleSelectTypeMode(chart.uuid)}
            removeChart={DashboardPageActions.removeChart}
            saveChart={this.saveChart}
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
  },

  render () {
    const dashboard = this.state.dashboard
    const charts = _.toArray(dashboard.charts)
    console.info('Dashboard.RENDER ========================================== Charts:', charts)
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={dashboard.title} save={this._toggleTitleEdit}/>
      :
      <h1 onClick={this._toggleTitleEdit}>
        <a>
          {dashboard.title || 'Untitled Dashboard'}
        </a>
      </h1>

    var temp = charts.slice();
    var arr = [];
    while (temp.length) {
      arr.push(temp.splice(0,1));
    }
    const chart_components = arr.map(row => {
      return (
        <div className='row collapse'>
          { this.renderChartRow(row) }
        </div>
      )
    })
    const loading = !charts.length > 0
    return (
      <section className='dashboard'>
        <header className='row dashboard-header'>
          <div className='medium-6 columns medium-text-left small-text-center'>
            { title_bar }
          </div>
          <div className='medium-6 columns medium-text-right small-text-center'>
            <button className='button' onClick={this.saveDashboard}>Save Dashboard</button>
          </div>
        </header>
        { loading ? <Placeholder height={600} /> : chart_components}
        { loading ? null : (
            <div className='row text-center'>
              <button
                className='button large'
                onClick={DashboardPageActions.addChart}
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
