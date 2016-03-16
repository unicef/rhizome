import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import DateRangePicker from 'components/molecules/DateRangePicker'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'

import ChartProperties from 'components/organisms/chart-wizard/ChartProperties'
import ChartPreview from 'components/organisms/chart-wizard/ChartPreview'

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
import IndicatorSelectorStore from 'stores/IndicatorSelectorStore'
import LocationSelectorStore from 'stores/LocationSelectorStore'
import DatapointStore from 'stores/DatapointStore'

import ChartActions from 'actions/ChartActions'
import ChartWizardActions from 'actions/ChartWizardActions'

const ChartWizard = React.createClass({
  mixins: [
    Reflux.connect(ChartStore, 'chart'),
    Reflux.connect(OfficeStore, 'offices'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators'),
    Reflux.connect(DatapointStore, 'datapoints'),
    Reflux.connect(IndicatorSelectorStore, 'selected_indicators'), // Try to get rid of these
    Reflux.connect(LocationSelectorStore, 'selected_locations') // Try to get rid of these
  ],

  defaultProps: {
    data: []
  },

  propTypes: {
    chart_id: PropTypes.number
  },

  componentDidMount () {
    IndicatorSelectorStore.listen(selected_indicators => {
      return ChartActions.setIndicatorIds(selected_indicators.map(indicator => indicator.id))
    })
    LocationSelectorStore.listen(selected_locations => {
      return ChartActions.setLocationIds(selected_locations.map(location => location.id))
    })
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
    const chart_def = this.state.chart.def
    const start_date = chart_def ? moment(chart_def.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart_def ? moment(chart_def.end_date, 'YYYY-MM-DD').toDate() : moment()

    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Explore Data</h1>
        <div className='medium-3 columns'>
          <div>
            <h3>Time</h3>
            <DateRangePicker
              sendValue={ChartActions.setDateRange}
              start={start_date}
              end={end_date}
              fromComponent='ChartWizard'
            />
          </div>
          <div className='row data-filters'>
            <br/>
            <IndicatorSelector
              indicators={this.state.indicators}
              preset_indicator_ids={[28, 31]}
              classes='medium-6 columns'
            />
            <LocationSelector
              locations={this.state.locations}
              preset_location_ids={[1]}
              classes='medium-6 columns'
            />
          </div>
        </div>
        <div className='medium-9 columns'>
          <ChartPreview chart={this.state.chart}/>
        </div>
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
