import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'
import api from 'data/api'

import Chart from 'components/molecules/Chart'
import DownloadButton from 'components/molecules/DownloadButton'
import DatabrowserTable from 'components/molecules/DatabrowserTable'

import ChartDataSelect from 'components/organisms/chart-wizard/ChartDataSelect'
import ChartProperties from 'components/organisms/chart-wizard/ChartProperties'
import PreviewScreen from 'components/organisms/chart-wizard/PreviewScreen'

import ChartWizardActions from 'actions/ChartWizardActions'
import ChartActions from 'actions/ChartActions'
import ChartWizardStore from 'stores/ChartWizardStore'
import ChartStore from 'stores/ChartStore'
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
    chart_id: PropTypes.number
  },

  mixins: [Reflux.connect(ChartWizardStore), Reflux.connect(ChartStore, 'ThisChart')],

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
        title: this.state.title,
        chart_json: JSON.stringify(this.state.chart.def)
      }
      api.post_chart(chart).then(res => {
        window.location.replace('/charts/' + res.objects.id)
      }, res => {
        console.log('update chart error,', res)
      })
    })
  },

  _downloadRawData: function () {
    let locations = this.state.locations.selected.map(location => location.id)
    let indicators = this.state.indicators.selected.map(indicator => indicator.id)
    let query = { 'format': 'csv' }

    if (indicators.length > 0) query.indicator__in = indicators
    if (locations.length > 0) query.location_id__in = locations
    if (this.state.chart.def.startDate) query.campaign_start = moment(this.state.chart.def.startDate).format('YYYY-M-D')
    if (this.state.chart.def.endDate) query.campaign_end = moment(this.state.chart.def.endDate).format('YYYY-M-D')

    return api.datapoints.toString(query)
  },

  render: function () {
    const data = this.state
    const chartDef = this.state.chart.def
    const start_date = chartDef ? moment(chartDef.startDate, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chartDef ? moment(chartDef.endDate, 'YYYY-MM-DD').toDate() : moment()

    if (!chartDef.type) {
      return null
    }

    const download_button = <DownloadButton onClick={this._downloadRawData} enable={this.state.rawData} text='Download Raw Data' working='Downloading' cookieName='dataBrowserCsvDownload'/>

    const chart = (
      <Chart
        id='custom-chart'
        type={chartDef.type}
        data={this.state.chart.data}
        options={this.state.chart.options}
        campaigns={this.state.campaigns.filtered}
        defaultCampaign={this.state.campaigns.selected}
      />
    )

    const location_options = [
      { title: 'by Status', value: this.state.location_lpd_statuses },
      { title: 'by Country', value: this.state.locations.filtered }
    ]

    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Explore Data</h1>
        <div className='row'>
          <ChartDataSelect
            start_date={start_date}
            end_date={end_date}
            all_indicators={this.state.indicators.list}
            all_locations={location_options}
            selected_indicators={this.state.indicators.selected}
            selected_locations={this.state.locations.selected}
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
                  data={this.state.rawData}
                  selected_locations={this.state.locations.selected}
                  selected_indicators={this.state.indicators.selected}
                />
              : <PreviewScreen isLoading={this.state.isLoading}>
                  {this.state.canDisplayChart ? chart : (<div className='empty'>No Data</div>) }
                </PreviewScreen>
            }
          </div>
        </div>
        <ChartProperties
          selected_chart_type={this.state.chart.def.type}
          selected_palette={this.state.chart.def.palette}
          chart_title={this.state.title}
          selectChartType={ChartWizardActions.changeChart}
          selectPalette={ChartWizardActions.changePalette}
          saveTitle={ChartWizardActions.editTitle}
          saveChart={this.saveChart}
          chartIsReady={!this.state.canDisplayChart}
        />
      </section>
    )
  }
})

export default ChartWizard
