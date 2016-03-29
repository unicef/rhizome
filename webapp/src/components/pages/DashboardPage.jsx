import _ from 'lodash'
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

  componentDidMount() {
    DashboardNewActions.addChart('RawData')
  },

  _showHideFooter () {
    this.setState({footerHidden: !this.state.footerHidden})
  },

  _addChart (type) {
    this.setState({footerHidden: true})
    DashboardNewActions.addChart(type)
  },

  render () {
    let charts = _.toArray(this.state.charts)
    console.info('Dashboard.RENDER ========================================== Charts:', charts)
    charts = charts.map(chart => {
      return (
        <div className='row'>
          <MultiChart
            chart={chart}
            removeChart={DashboardNewActions.removeChart}
            setDateRange={(key, value) => DashboardNewActions.setDateRange(key, value, chart.uuid)}
            setPalette={(palette) => DashboardNewActions.setPalette(palette, chart.uuid)}
            setTitle={(title) => DashboardNewActions.setTitle(title, chart.uuid)}
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
