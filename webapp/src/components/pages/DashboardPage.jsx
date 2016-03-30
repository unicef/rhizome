import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import MultiChart from 'components/organisms/MultiChart'

import RootStore from 'stores/RootStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardNewStore from 'stores/DashboardNewStore'

import DashboardNewActions from 'actions/DashboardNewActions'
import ChartActions from 'actions/ChartActions'

const Dashboard = React.createClass({

  mixins: [
    Reflux.connect(DashboardNewStore, 'charts'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    chart_id: PropTypes.number
  },

  componentDidMount () {
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index) {
        DashboardNewActions.addChart()
      }
    })
  },

  saveChart (chart) {
    console.info('- Dashboard.saveChart')
    if (!chart.title || chart.title === 'Untitled') {
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
    let charts = _.toArray(this.state.charts)
    console.info('Dashboard.RENDER ========================================== Charts:', charts)
    charts = charts.map(chart => {
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
            setTitle={(title) => DashboardNewActions.setTitle(title, chart.uuid)}
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
          <hr />
        </div>
      )
    })

    return (
      <section className='dashboard'>
        { charts }
        <button
          className='button expand fix-to-bottom'
          onClick={DashboardNewActions.addChart}
          style={{paddingTop: '1rem', paddingBottom: '1rem', position: 'fixed', bottom: '2.6rem'}}>
          Add Chart
        </button>
      </section>
    )
  }
})

export default Dashboard
