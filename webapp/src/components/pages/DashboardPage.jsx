import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import MultiChart from 'components/organisms/MultiChart'

import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import OfficeStore from 'stores/OfficeStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardNewStore from 'stores/DashboardNewStore'
import DashboardNewActions from 'actions/DashboardNewActions'

const Dashboard = React.createClass({

  mixins: [
    Reflux.connect(DashboardNewStore, 'charts'),
    Reflux.connect(OfficeStore, 'offices'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    chart_id: PropTypes.number
  },

  render () {
    console.info('Dashboard.RENDER ==========================================')
    const charts = this.state.charts.map((chart, index) => {
      return (
        <div>
          <MultiChart
            chart={chart}
            chart_id={7}
            removeChart={DashboardNewActions.removeChart}
            setIndicators={(indicators) => DashboardNewActions.setIndicators(indicators, index)}
            selectIndicator={(id) => DashboardNewActions.selectIndicator(id, index)}
            deselectIndicator={(id) => DashboardNewActions.deselectIndicator(id, index)}
            reorderIndicator={(indicators) => DashboardNewActions.reorderIndicator(indicators, index)}
            clearSelectedIndicators={() => DashboardNewActions.clearSelectedIndicators(index)}
            setLocations={(locations) => DashboardNewActions.setLocations(locations, index)}
            selectLocation={(id) => DashboardNewActions.selectLocation(id, index)}
            deselectLocation={(id) => DashboardNewActions.deselectLocation(id, index)}
            clearSelectedLocations={() => DashboardNewActions.clearSelectedLocations(index)}
            setCampaigns={(campaigns) => DashboardNewActions.setCampaigns(campaigns, index)}
            selectCampaign={(id) => DashboardNewActions.selectCampaign(id, index)}
            deselectCampaign={(id) => DashboardNewActions.deselectCampaign(id, index)}
            setDateRange={(key, value) => DashboardNewActions.setDateRange(key, value, index)}
            setPalette={(palette) => DashboardNewActions.setPalette(palette, index)}
            setTitle={(title) => DashboardNewActions.setTitle(title, index)}
            setType={(type) => DashboardNewActions.setType(type, index)}
          />
          <hr />
        </div>
      )
    })
    return (
      <section className='multi-chart'>
        { charts }
        <button
          className='button expand'
          onClick={DashboardNewActions.addChart}
          style={{paddingTop: '1rem', paddingBottom: '1rem'}}
        >
          Add Chart
        </button>
      </section>
    )
  }
})

export default Dashboard
