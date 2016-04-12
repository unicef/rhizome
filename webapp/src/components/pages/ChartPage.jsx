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

const ChartPage = React.createClass({

  mixins: [
    Reflux.connect(DashboardPageStore, 'dashboard'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    chart_id: PropTypes.number
  },

  getInitialState () { console.log('ChartPage.getInitialState')
    return {
      titleEditMode: false
    }
  },

  componentDidMount () { console.log('ChartPage.componentDidMount')
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index) {
        if (this.props.chart_id) {
          DashboardPageActions.fetchChart(this.props.chart_id)
        } else {
          DashboardPageActions.addChart()
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

  shouldComponentUpdate(nextProps, nextState) { console.log('ChartPage.shouldComponentUpdate')
    const charts = _.toArray(nextState.dashboard.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    return !this.missing_data || this.missing_params || this.loading_charts
  },

  saveChart (chart) { console.log('ChartPage.saveChart')
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

  render () { console.log('ChartPage.render')
    const loading = !this.state.dashboard.charts.length > 0
    const chart = _.toArray(this.state.dashboard.charts)[0]

    return chart ? (
      <div className='row'>
        <MultiChart
          chart={chart}
          linkCampaigns={() => DashboardPageActions.toggleCampaignLink(chart.uuid)}
          toggleSelectTypeMode={() => DashboardPageActions.toggleSelectTypeMode(chart.uuid)}
          toggleEditMode={() => DashboardPageActions.toggleEditMode(chart.uuid)}
          saveChart={() => this.saveChart(chart)}
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
    ) : <Placeholder height={600} />
  }
})

export default ChartPage
