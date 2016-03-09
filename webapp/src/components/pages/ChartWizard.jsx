import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'
import api from 'data/api'

import DateRangePicker from 'components/molecules/DateRangePicker'
import DownloadButton from 'components/molecules/DownloadButton'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import List from 'components/molecules/list/List'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import Chart from 'components/molecules/Chart'

import ChartDataSelect from 'components/organisms/chart-wizard/ChartDataSelect'
import ChartProperties from 'components/organisms/chart-wizard/ChartProperties'
import PreviewScreen from 'components/organisms/chart-wizard/PreviewScreen'

import ChartWizardActions from 'actions/ChartWizardActions'
import DataFiltersStore from 'stores/DataFiltersStore'
import ChartWizardStore from 'stores/ChartWizardStore'
import ChartAPI from 'data/requests/ChartAPI'

const defaultChartDef = {
  type: 'RawData',
  indicator_ids: [],
  location_ids: [],
  countries: [],
  groupBy: 'indicator',
  timeRange: null,
  x: 0,
  xFormat: ',.0f',
  y: 0,
  yFormat: ',.0f',
  z: 0
}

let ChartWizard = React.createClass({
  propTypes: {
    chartDef: PropTypes.object,
    chart_id: PropTypes.number,
    save: PropTypes.func,
    cancel: PropTypes.func
  },

  mixins: [Reflux.connect(ChartWizardStore, 'data'), Reflux.connect(DataFiltersStore, 'raw_data')],

  componentDidMount () {
    if (this.props.chart_id) {
      ChartAPI.getChart(this.props.chart_id).then(response => ChartWizardActions.initialize(response))
    } else {
      this.chartDef = this.props.chartDef || defaultChartDef
      ChartWizardActions.initialize(this.chartDef)
    }
  },

  componentWillReceiveProps () {
    ChartWizardActions.clear()
  },

  saveChart () {
    ChartWizardActions.saveChart(data => {
      var chart = {
        id: this.props.chart_id,
        title: this.state.data.title,
        chart_json: JSON.stringify(this.state.data.chartDef)
      }
      api.post_chart(chart).then(res => {
        window.location.replace('/charts/' + res.objects.id)
      }, res => {
        console.log('update chart error,', res)
      })
    })
  },

  _downloadRawData: function () {
    let locations = this.state.data.selectedLocations.map(location => { return location.id })
    let indicators = this.state.data.selectedIndicators.map(indicator => { return indicator.id })
    let query = { 'format': 'csv' }

    if (indicators.length > 0) query.indicator__in = indicators
    if (locations.length > 0) query.location_id__in = locations
    if (this.state.data.chartDef.startDate) query.campaign_start = moment(this.state.data.chartDef.startDate).format('YYYY-M-D')
    if (this.state.data.chartDef.endDate) query.campaign_end = moment(this.state.data.chartDef.endDate).format('YYYY-M-D')

    return api.datapoints.toString(query)
  },

  render: function () {
    const data = this.state.data
    const chartDef = data.chartDef
    const start_date = chartDef ? moment(chartDef.startDate, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chartDef ? moment(chartDef.endDate, 'YYYY-MM-DD').toDate() : moment()

    if (!chartDef.type)
      return null
    }

    const download_button = <DownloadButton onClick={this._downloadRawData} enable={data.rawData} text='Download Raw Data' working='Downloading' cookieName='dataBrowserCsvDownload'/>

    const chart = (
      <Chart
        id='custom-chart'
        type={chartDef.type}
        data={data.chartData}
        options={data.chartOptions}
        campaings={data.campaignFilteredList}
        defaultCampaign={data.campaign}
      />
    )

    const location_options = [
      { title: 'by Status', value: data.location_lpd_statuses },
      { title: 'by Country', value: data.locationFilteredList }
    ]

    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Explore Data</h1>
        <div className='row'>
          <ChartDataSelect
            start_date={start_date}
            end_date={end_date}
            all_indicators={data.indicatorList}
            all_locations={location_options}
            selected_indicators={data.selectedIndicators}
            selected_locations={data.selectedLocations}
            addLocation={ChartWizardActions.addLocation}
            removeLocation={ChartWizardActions.removeLocation}
            addIndicator={ChartWizardActions.addIndicator}
            reorderIndicator={ChartWizardActions.reorderIndicator}
            removeIndicator={ChartWizardActions.removeIndicator}
            clearSelectedIndicators={ChartWizardActions.clearSelectedIndicators}
            clearSelectedLocations={ChartWizardActions.clearSelectedLocations}
            setDateRange={ChartWizardActions.updateDateRangePicker}
          />
          <div className='medium-9 columns'>
            {
              chartDef.type === 'RawData'
              ? <DatabrowserTable
                  data={data.rawData}
                  selected_locations={data.selectedLocations}
                  selected_indicators={data.selectedIndicators}
                />
              : <PreviewScreen isLoading={data.isLoading}>
                  {data.canDisplayChart ? chart : (<div className='empty'>No Data</div>) }
                </PreviewScreen>
            }
          </div>
        </div>
        <ChartProperties
          selected_chart_type={data.chartDef.type}
          selected_palette={data.chartDef.palette}
          chart_title={data.title}
          selectChartType={ChartWizardActions.changeChart}
          selectPalette={ChartWizardActions.changePalette}
          saveTitle={ChartWizardActions.editTitle}
          saveChart={this.saveChart}
          chartIsReady={!data.canDisplayChart}
        />
      </section>
    )
  }
})

export default ChartWizard
