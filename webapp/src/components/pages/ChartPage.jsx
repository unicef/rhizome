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
import DashboardChartsStore from 'stores/DashboardChartsStore'

import DashboardChartsActions from 'actions/DashboardChartsActions'
import ChartActions from 'actions/ChartActions'
import DashboardActions from 'actions/DashboardActions'

const ChartPage = React.createClass({

  mixins: [
    Reflux.connect(DashboardChartsStore, 'charts'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    chart_id: PropTypes.number
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
        if (this.props.chart_id) {
          DashboardChartsActions.fetchChart(this.props.chart_id)
        } else {
          DashboardChartsActions.addChart()
        }
      }
    })
    this.listenTo(ChartActions.postChart.completed, (response) => {
      if (!this.props.chart_id) {
        const chart_id = response.objects.id
        window.location = window.location.origin + '/charts/' + chart_id
      }
    })
  },

  shouldComponentUpdate(nextProps, nextState) {
    const charts = _.toArray(nextState.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    return !this.missing_data || this.missing_params || this.loading_charts
  },

  saveChart (chart) {
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
        indicator_ids: chart.selected_indicators.map(indicator => indicator.id),
        groupBy: chart.groupBy,
        groupByTime: chart.groupByTime
      })
    })
  },

  render () {
    const loading = !this.state.charts.length > 0
    const chart = _.toArray(this.state.charts)[0]

    return chart ? (
      <div className='row'>
        <MultiChart
          chart={chart}
          linkCampaigns={() => DashboardChartsActions.toggleCampaignLink(chart.uuid)}
          toggleSelectTypeMode={() => DashboardChartsActions.toggleSelectTypeMode(chart.uuid)}
          toggleEditMode={() => DashboardChartsActions.toggleChartEditMode(chart.uuid)}
          saveChart={() => this.saveChart(chart)}
          setDateRange={(key, value) => DashboardChartsActions.setDateRange(key, value, chart.uuid)}
          setGroupByTime={(grouping) => DashboardChartsActions.setGroupByTime(grouping, chart.uuid)}
          setGroupBy={(grouping) => DashboardChartsActions.setGroupBy(grouping, chart.uuid)}
          setPalette={(palette) => DashboardChartsActions.setPalette(palette, chart.uuid)}
          setTitle={(title) => DashboardChartsActions.setChartTitle(title, chart.uuid)}
          setType={(type) => DashboardChartsActions.setType(type, chart.uuid)}
          setIndicators={(indicators) => DashboardChartsActions.setIndicators(indicators, chart.uuid)}
          setIndicatorFilter={(filter) => DashboardChartsActions.setIndicatorFilter(filter, chart.uuid)}
          selectIndicator={(id) => DashboardChartsActions.selectIndicator(id, chart.uuid)}
          deselectIndicator={(id) => DashboardChartsActions.deselectIndicator(id, chart.uuid)}
          reorderIndicator={(indicators) => DashboardChartsActions.reorderIndicator(indicators, chart.uuid)}
          clearSelectedIndicators={() => DashboardChartsActions.clearSelectedIndicators(chart.uuid)}
          setLocations={(locations) => DashboardChartsActions.setLocations(locations, chart.uuid)}
          selectLocation={(id) => DashboardChartsActions.selectLocation(id, chart.uuid)}
          deselectLocation={(id) => DashboardChartsActions.deselectLocation(id, chart.uuid)}
          clearSelectedLocations={() => DashboardChartsActions.clearSelectedLocations(chart.uuid)}
          setCampaigns={(campaigns) => DashboardChartsActions.setCampaigns(campaigns, chart.uuid)}
          selectCampaign={(id) => DashboardChartsActions.selectCampaign(id, chart.uuid)}
          deselectCampaign={(id) => DashboardChartsActions.deselectCampaign(id, chart.uuid)}
        />
      </div>
    ) : <Placeholder height={600} />
  }
})

export default ChartPage
