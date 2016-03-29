import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import Notification from 'react-notification'

import MultiChart from 'components/organisms/MultiChart'

import PalettePicker from 'components/organisms/data-explorer/preview/PalettePicker'
import ChartSelect from 'components/organisms/data-explorer/ChartSelect'
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

  getInitialState () {
    return {
      notification: true,
      footerHidden: true
    }
  },

  _showHideFooter () { console.info('Dashboard._showHideFooter')
    this.setState({footerHidden: !this.state.footerHidden})
  },

  _addChart (type) {
    this.setState({footerHidden: true})
    DashboardNewActions.addChart(type)
  },

  render () {
    console.info('Dashboard.RENDER ==========================================')
    const charts = this.state.charts.map((chart, index) => {
      return (
        <div className='row'>
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
          />
          <hr />
        </div>
      )
    })

    return (
      <section className='dashboard'>
        { charts }
        <footer className={'row hideable text-center' + (this.state.footerHidden ? ' descended' : '')}>
            <h4>Select a Chart Type</h4>
            <ChartSelect onChange={this._addChart}/>
        </footer>
        <button
          className='button expand fix-to-bottom'
          onClick={this._showHideFooter}
          style={{paddingTop: '1rem', paddingBottom: '1rem', position: 'fixed', bottom: '2.6rem'}}>
          { this.state.footerHidden ? ' Add Chart' : 'Cancel'}
        </button>
      </section>
    )
  }
})

export default Dashboard
