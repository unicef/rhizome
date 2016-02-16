import React from 'react'
import Reflux from 'reflux'
import moment from 'moment'
import api from 'data/api'

import DateRangePicker from '02-molecules/DateRangePicker'
import DownloadButton from '02-molecules/DownloadButton'
import DatabrowserTable from '02-molecules/DatabrowserTable'
import TitleInput from '02-molecules/TitleInput'
import List from '02-molecules/list/List'
import ReorderableList from '02-molecules/list/ReorderableList'
import DropdownMenu from '02-molecules/menus/DropdownMenu'
import Chart from '02-molecules/Chart'

import PreviewScreen from '03-organisms/chart-wizard/PreviewScreen'
import ChartSelect from '03-organisms/chart-wizard/ChartSelect'
import PalettePicker from '03-organisms/chart-wizard/preview/PalettePicker'

import ChartWizardActions from 'actions/ChartWizardActions'
import DataFiltersStore from 'stores/DataFiltersStore'
import ChartWizardStore from 'stores/ChartWizardStore'
import ChartAPI from 'data/requests/ChartAPI'

const defaultChartDef = {
  title: '',
  type: 'LineChart',
  indicators: [],
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
    chartDef: React.PropTypes.object,
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  mixins: [Reflux.connect(ChartWizardStore, 'data'), Reflux.connect(DataFiltersStore, 'raw_data')],

  componentDidMount () {
    if (this.props.chart_id) {
      ChartAPI.getChart(this.props.chart_id).then(function(response){
        let chart_json = response.chart_json
        ChartWizardActions.initialize(chart_json)
      })
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
        chart_json: JSON.stringify(this.state.data.chartDef)
      }
      api.post_chart(chart).then(res => {
        window.location.replace("/datapoints/charts/" + res.objects.id);
      }, res => {
        console.log('update chart error,', res)
      })
    })
  },

  toggleStep (refer) {
    return () => {
      this.setState({
        refer: refer
      })
    }
  },

  setLocationSearch: function (pattern) {
    this.setState({
      locationSearch: pattern
    })
  },

  _downloadRawData: function () {
    let locations = this.state.data.selected_locations.map(location => { return location.id })
    let indicators = this.state.data.indicatorSelected.map(indicator => { return indicator.id })
    let query = { 'format': 'csv' }

    if (indicators.length > 0) query.indicator__in = indicators
    if (locations.length > 0) query.location_id__in = locations
    if (this.state.data.campaign.start_date) query.campaign_start = moment(this.state.data.campaign.start_date).format('YYYY-M-D')
    if (this.state.data.campaign.end_date) query.campaign_end = moment(this.state.data.campaign.end_date).format('YYYY-M-D')

    return api.datapoints.toString(query)
  },

  render: function () {
    let availableIndicators = this.state.data.indicatorList
    let palette = this.state.data.chartDef.palette || 'orange'
    let startDate = moment()
    let endDate = moment()

    if (this.state.data.chartDef) {
      startDate = moment(this.state.data.chartDef.startDate, 'YYYY-MM-DD').toDate()
      endDate = moment(this.state.data.chartDef.endDate, 'YYYY-MM-DD').toDate()
    }

    if (!this.state.data.chartDef.type) {
      return null
    }

    let chart = (
      <Chart
          id='custom-chart'
          type={this.state.data.chartDef.type}
          data={this.state.data.chartData}
          options={this.state.data.chartOptions}
          campaings={this.state.data.campaignFilteredList}
          defaultCampaign={this.state.data.campaign}
          />
    )

    let location_options = [
      { title: 'by Tag', value: this.state.data.location_tags },
      { title: 'by Country', value: this.state.data.locationFilteredList }
    ]

    let clear_locations_button = ''
    if (this.state.data.selected_locations.length > 3) {
      clear_locations_button = <a className='remove-filters-link' onClick={ChartWizardActions.clearSelectedLocations}>Remove All </a>
    }

    let clear_indicators_button = ''
    if (this.state.data.indicatorSelected.length > 3) {
      clear_indicators_button = <a className='remove-filters-link' onClick={ChartWizardActions.clearSelectedIndicators}>Remove All </a>
    }

    let call_to_action = <button className='right button success' disabled={!this.state.data.canDisplayChart} onClick={this.saveChart} ><i className='fa fa-save'></i> &nbsp; Save Chart</button>
    if (this.state.data.chartDef.type === 'RawData') {
      call_to_action = <DownloadButton onClick={this._downloadRawData} enable={this.state.data.rawData} text='Download Raw Data' working='Downloading' cookieName='dataBrowserCsvDownload'/>
    }

    let data_output = (
      <PreviewScreen isLoading={this.state.data.isLoading}>
        {this.state.data.canDisplayChart ? chart : (<div className='empty'>No Data</div>) }
      </PreviewScreen>
    )

    if (this.state.data.chartDef.type === 'RawData') {
      data_output = <DatabrowserTable data={this.state.data.rawData} selected_locations={this.state.data.selected_locations} selected_indicators={this.state.data.indicatorSelected} />
    }

    let title_input = <TitleInput save={ChartWizardActions.editTitle}/>
    if (this.state.data.chartDef) {
      title_input = <TitleInput initialText={this.state.data.chartDef.title} save={ChartWizardActions.editTitle}/>
    }


    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Explore Data</h1>
        <div className='row'>
          <div className='medium-3 columns'>
            <div>
              <h3>Time</h3>
              <DateRangePicker
                sendValue={ChartWizardActions.updateDateRangePicker}
                start={startDate}
                end={endDate}
                fromComponent='ChartWizard' />
              <br/>
            </div>
            <div className='row data-filters'>
              <br/>
              <div className='medium-6 columns'>
                  <h3>
                    Indicators
                    <DropdownMenu
                      items={availableIndicators}
                      sendValue={ChartWizardActions.addIndicator}
                      item_plural_name='Indicators'
                      style='icon-button right'
                      icon='fa-plus' />
                  </h3>
                  {clear_indicators_button}
                  <ReorderableList items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator} dragItem={ChartWizardActions.reorderIndicator} />
              </div>
              <div className='medium-6 columns'>
                <h3>
                  Locations
                  <DropdownMenu
                    items={location_options}
                    sendValue={ChartWizardActions.addLocation}
                    item_plural_name='Locations'
                    style='icon-button right'
                    icon='fa-plus'
                    grouped/>
                </h3>
                {clear_locations_button}
                <List items={this.state.data.selected_locations} removeItem={ChartWizardActions.removeLocation} />
                <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
              </div>
            </div>
          </div>
          <div className='medium-9 columns'>
              { data_output }
          </div>
        </div>
        <footer className='row'>
          <div className='medium-4 columns'>
            <h3>Chart Type</h3>
            <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
                onChange={ChartWizardActions.changeChart}/>
          </div>
          <div className='medium-4 columns'>
            <h3>Color Scheme</h3>
            <PalettePicker value={palette} onChange={ChartWizardActions.changePalette}/>
          </div>
          <div className='medium-4 columns'>
            <div className='medium-8 columns'>
              <h3>Chart Title</h3>
              { title_input }
            </div>
            <div className='medium-4 columns'>
              { call_to_action }
            </div>
          </div>
        </footer>
      </section>
    )
  }
})

export default ChartWizard
