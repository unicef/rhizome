import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import ChartDataSelect from 'components/organisms/chart-wizard/ChartDataSelect'
import ChartProperties from 'components/organisms/chart-wizard/ChartProperties'

import ChartInit from 'components/molecules/charts_d3/ChartInit'
import Chart from 'components/molecules/Chart'
import DownloadButton from 'components/molecules/DownloadButton'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import PreviewScreen from 'components/organisms/chart-wizard/PreviewScreen'

import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import OfficeStore from 'stores/OfficeStore'
import CampaignStore from 'stores/CampaignStore'
import ChartStore from 'stores/ChartStore'

import ChartWizardActions from 'actions/ChartWizardActions'

const ChartWizard = React.createClass({
  mixins: [
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(IndicatorStore, 'indicators'),
    Reflux.connect(OfficeStore, 'offices'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(ChartStore, 'chart')
  ],

  defaultProps: {
    data: []
  },

  propTypes: {
    chart_id: PropTypes.number
  },

  initDataReady () {
    const locationsReady = !_.isEmpty(this.state.locations.raw)
    const indicatorsReady = !_.isEmpty(this.state.indicators.raw)
    const campaignsReady = !_.isEmpty(this.state.campaigns.raw)
    const officesReady = !_.isEmpty(this.state.offices.raw)
    return locationsReady && indicatorsReady && campaignsReady && officesReady
  },

  shouldComponentUpdate (nextProps, nextState) {
    return this.initDataReady()
  },

  render () {
    if (!this.initDataReady()) {
      return <div>Loading...</div>
    }
    const chart = this.state.chart
    const start_date = chart.def ? moment(chart.def.startDate, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart.def ? moment(chart.def.endDate, 'YYYY-MM-DD').toDate() : moment()

    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Explore Data</h1>
        <ChartDataSelect
          start_date={start_date}
          end_date={end_date}
          indicators={this.state.indicators}
          locations={this.state.locations}
          setDateRange={ChartWizardActions.updateDateRangePicker} />
        <ChartProperties
          selected_chart_type={this.state.chart.def.type}
          selected_palette={this.state.chart.def.palette}
          chart_title={this.state.title}
          selectChartType={ChartWizardActions.changeChart}
          selectPalette={ChartWizardActions.changePalette}
          saveTitle={ChartWizardActions.editTitle}
          saveChart={this.saveChart}
          chartIsReady={!this.state.canDisplayChart} />
      </section>
    )
  }
})

export default ChartWizard
