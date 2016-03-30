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
            removeChart={DashboardNewActions.removeChart}
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
