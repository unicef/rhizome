import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import Placeholder from 'components/Placeholder'
import MultiChart from 'components/organisms/multi-chart/MultiChart'
import TitleInput from 'components/TitleInput'

import RootStore from 'stores/RootStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardChartsStore from 'stores/DashboardChartsStore'

import DashboardChartsActions from 'actions/DashboardChartsActions'
import ChartActions from 'actions/ChartActions'
import DashboardActions from 'actions/DashboardActions'

const ChartContainer = React.createClass({

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
          saveChart={() => DashboardChartsActions.saveChart(chart.uuid)}
          updateTypeParams={(key, value) => DashboardChartsActions.updateTypeParams(key, value, chart.uuid)}
          setDateRange={(key, value) => DashboardChartsActions.setDateRange(key, value, chart.uuid)}
          setGroupByTime={(grouping) => DashboardChartsActions.setGroupByTime(grouping, chart.uuid)}
          setGroupBy={(grouping) => DashboardChartsActions.setGroupBy(grouping, chart.uuid)}
          setPalette={(palette) => DashboardChartsActions.setPalette(palette, chart.uuid)}
          setTitle={(title) => DashboardChartsActions.setChartTitle(title, chart.uuid)}
          setType={(type) => DashboardChartsActions.setType(type, chart.uuid)}
          setIndicators={(indicators) => DashboardChartsActions.setIndicators(indicators, chart.uuid)}
          setIndicatorFilter={(filter) => DashboardChartsActions.setIndicatorFilter(filter, chart.uuid)}
          setIndicatorColor={(indicator, color) => DashboardChartsActions.setIndicatorColor(indicator, color, chart.uuid)}
          selectIndicator={(id) => DashboardChartsActions.selectIndicator(id, chart.uuid)}
          deselectIndicator={(id) => DashboardChartsActions.deselectIndicator(id, chart.uuid)}
          reorderIndicator={(indicators) => DashboardChartsActions.reorderIndicator(indicators, chart.uuid)}
          clearSelectedIndicators={() => DashboardChartsActions.clearSelectedIndicators(chart.uuid)}
          setLocationDepth={depth => DashboardChartsActions.setLocationDepth(depth, chart.uuid)}
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

export default ChartContainer
