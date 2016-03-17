import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import DropdownList from 'react-widgets/lib/DropdownList'
import DateRangePicker from 'components/molecules/DateRangePicker'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'

import ChartProperties from 'components/organisms/chart-wizard/ChartProperties'

import ChartInfo from 'components/molecules/charts_d3/ChartInfo'
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
    Reflux.connect(DatapointStore, 'datapoints')
  ],

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
    const chart = this.state.chart
    const start_date = chart.def ? moment(chart.def.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart.def ? moment(chart.def.end_date, 'YYYY-MM-DD').toDate() : moment()

    const loading_component = (
      <div className='loading'>
        <i className='fa fa-spinner fa-spin fa-5x'></i>
        <div>Loading</div>
      </div>
    )

    const chart_component = (
      <Chart type={chart.def.type} data={chart.data} options={chart.def} />
    )

    const sidebar_component = (
      <div>
        <div>
          <h3>Time</h3>
          <DateRangePicker
            sendValue={ChartActions.setDateRange}
            start={start_date}
            end={end_date}
            fromComponent='ChartWizard'
          />
          <br/>
        </div>
        <div className='row collapse'>
          <h3>Campaign</h3>
          <DropdownList
            data={this.state.campaigns.raw}
            defaultValue={this.state.campaigns.raw ? this.state.campaigns.raw[0].id : null}
            textField='name'
            valueField='id'
            onChange={campaign => ChartActions.setCampaignIds([campaign.id])}
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
    )

    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Explore Data</h1>
        <div className='medium-3 columns'>
          {this.initDataReady() ? sidebar_component : loading_component}
        </div>
        <div className='medium-9 columns'>
          {!_.isEmpty(chart.data) ? chart_component : loading_component}
        </div>
        <ChartProperties
          selected_chart_type={this.state.chart.def.type}
          selected_palette={this.state.chart.def.palette}
          chart_title={this.state.chart.def.title}
          selectChartType={ChartActions.setType}
          selectPalette={ChartActions.setPalette}
          saveTitle={ChartActions.setTitle}
          saveChart={this.saveChart}
          chartIsReady={!this.state.canDisplayChart} />
      </section>
    )
  }
})

export default ChartWizard
