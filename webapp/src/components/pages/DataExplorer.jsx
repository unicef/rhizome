import _ from 'lodash'
import api from 'data/api'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import PalettePicker from 'components/organisms/data-explorer/preview/PalettePicker'
import ChartSelect from 'components/organisms/data-explorer/ChartSelect'

import CampaignTitleMenu from 'components/molecules/menus/CampaignTitleMenu'
import builderDefinitions from 'components/molecules/charts/utils/builderDefinitions'
import Chart from 'components/molecules/charts/Chart'
import ExportPdf from 'components/molecules/ExportPdf'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import DownloadButton from 'components/molecules/DownloadButton'
import DateRangePicker from 'components/molecules/DateRangePicker'
import Placeholder from 'components/molecules/Placeholder'
import TitleInput from 'components/molecules/TitleInput'

import IndicatorSelectorStore from 'stores/IndicatorSelectorStore'
import LocationSelectorStore from 'stores/LocationSelectorStore'
import LocationStore from 'stores/LocationStore'
import ChartStore from 'stores/ChartStore'
import IndicatorStore from 'stores/IndicatorStore'
import OfficeStore from 'stores/OfficeStore'
import CampaignStore from 'stores/CampaignStore'
import DataExplorerStore from 'stores/DataExplorerStore'
import RootStore from 'stores/RootStore'
import DatapointStore from 'stores/DatapointStore'
import TableChart from 'components/molecules/charts/TableChart'
import LineChart from 'components/molecules/charts/LineChart'
import ChoroplethMap from 'components/molecules/charts/ChoroplethMap'

import DataExplorerActions from 'actions/DataExplorerActions'
import IndicatorSelectorActions from 'actions/IndicatorSelectorActions'
import ChartActions from 'actions/ChartActions'

const DataExplorer = React.createClass({
  mixins: [
    Reflux.connect(DataExplorerStore, 'chart'),
    Reflux.connect(ChartStore, 'charts'),
    Reflux.connect(OfficeStore, 'offices'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators'),
    Reflux.connect(DatapointStore, 'datapoints')
  ],

  getInitialState () {
    return {
      footerHidden: false,
      titleEditMode: false
    }
  },

  propTypes: {
    chart_id: PropTypes.number
  },

  componentDidMount () {
    if (this.props.chart_id) { this.setState({footerHidden: true}) }
    RootStore.listen( this.getChart)

    this.joinTrailing(LocationStore, LocationSelectorStore, IndicatorStore, IndicatorSelectorStore,
      CampaignStore, this.setInitialData)
  },

  setInitialData (locations, selected_locations, indicators, selected_indicators, campaigns) {
    // joinTrailing delivers everythign in a 1 item array for some reason
    DataExplorerActions.setIndicators(selected_indicators[0])
    DataExplorerActions.setLocations(selected_locations[0])
    DataExplorerActions.setCampaigns(campaigns[0].raw[0])
  },

  getChart () {
    const dataIsReady = this.state.locations.index && this.state.indicators.index && this.state.charts.index
    if (this.props.chart_id && dataIsReady) {
      DataExplorerActions.fetchChart.completed(this.state.charts.index[this.props.chart_id])
    }
  },

  // =========================================================================== //
  //                                EVENT HANDLERS                               //
  // =========================================================================== //
  _saveChart () {
    const chart = this.state.chart
    if (!chart.title) {
      return window.alert('Please add a Title to your chart')
    }
    ChartActions.postChart({
      id: this.props.chart_id,
      title: chart.title,
      chart_json: JSON.stringify({
        type: chart.type,
        start_date: chart.start_date,
        end_date: chart.end_date,
        campaign_ids: chart.selected_campaigns.map(campaign => campaign.id),
        location_ids: chart.selected_locations.map(location => location.id),
        indicator_ids: chart.selected_indicators.map(indicator => indicator.id)
      })
    })
  },

  _showHideFooter () {
    this.setState({footerHidden: !this.state.footerHidden})
  },

  _toggleTitleEdit (title) {
    if (_.isString(title)) {
      DataExplorerActions.setTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  // =========================================================================== //
  //                                    RENDER                                   //
  // =========================================================================== //
  getChartComponentByType(type) {
    if (type === 'TableChart') {
      return <TableChart {...this.state.chart} />
    } else if (type === 'LineChart') {
      return <LineChart {...this.state.chart} />
    } else if (type === 'ChoroplethMap') {
      return <ChoroplethMap {...this.state.chart} />
    }
  },

  render () {
    const chart = this.state.chart
    const start_date = chart ? moment(chart.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart ? moment(chart.end_date, 'YYYY-MM-DD').toDate() : moment()
    const disableSave = _.isEmpty(chart.selected_locations) || _.isEmpty(chart.selected_indicators)
    const preset_indicator_ids = this.props.chart_id && chart ? chart.selected_indicators.map(indicator => indicator.id) : [27]
    const preset_location_ids = this.props.chart_id && chart ? chart.selected_locations.map(location => location.id) : [1]
    const multi_indicator = chart.type === 'TableChart' || chart.type === 'RawData'
    const multi_location = chart.type === 'TableChart' || chart.type === 'RawData'
    const raw_data_query = {
      format: 'csv',
      indicator__in: chart.selected_indicators.map(indicator => indicator.id),
      location__in: chart.selected_locations.map(location => location.id),
      campaign_start: start_date,
      campaign_end: end_date
    }
    // CHART
    // ---------------------------------------------------------------------------
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={chart.title} save={this._toggleTitleEdit}/>
      :
      <h1>
        {chart.title}
        <a className='button icon-button' onClick={this._toggleTitleEdit}><i className='fa fa-pencil'/></a>
      </h1>

    const chart_component = chart.type === 'RawData'?
      <DatabrowserTable
        data={this.state.datapoints.raw}
        selected_locations={chart.selected_locations}
        selected_indicators={chart.selected_indicators}
      />
      : this.getChartComponentByType(chart.type)

    // SIDEBAR
    // ---------------------------------------------------------------------------
    const call_to_actions = (
      <div className='row collapse'>
        <button className='expand button success' disabled={disableSave} onClick={this._saveChart} style={{marginTop: 0}}>
          <i className='fa fa-save'></i> {this.props.chart_id ? 'Save Chart' : 'Save To Charts'}
        </button>
        <ExportPdf className='expand' button disabled={disableSave}/>
        <DownloadButton
          onClick={() => api.datapoints.toString(raw_data_query)}
          enable={this.state.datapoints.raw ? true : false}
          text='Download Data'
          working='Downloading'
          cookieName='dataBrowserCsvDownload'/>
      </div>
    )

    const date_range_picker = chart.type === 'LineChart' ? (
      <div className='medium-12 columns'>
        <h3>Time</h3>
        <DateRangePicker
          sendValue={DataExplorerActions.setDateRange}
          start={start_date}
          end={end_date}
          fromComponent='DataExplorer'
        />
        <br/>
      </div>
    ) : ''

    const campaign_dropdown = chart.type !== 'LineChart' && !_.isEmpty(this.state.campaigns.raw) && !_.isEmpty(chart.selected_campaigns)
      ? (
        <div className='row collapse'>
          <h3>Campaign</h3>
          <CampaignTitleMenu
            campaigns={this.state.campaigns.raw}
            selected={_.isEmpty(chart.selected_campaigns) ? null : chart.selected_campaigns[0]}
            sendValue={DataExplorerActions.setCampaigns}/>
        </div>
      ) : <Placeholder height={100}/>

    const location_selector = (
      <LocationSelector
        locations={this.state.locations}
        preset_location_ids={preset_location_ids}
        classes={multi_location ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multi_location}
      />
    )

    const indicator_selector = (
      <IndicatorSelector
        indicators={this.state.indicators}
        preset_indicator_ids={preset_indicator_ids}
        classes={multi_indicator ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multi_indicator}
      />
    )

    // FOOTER
    // ---------------------------------------------------------------------------
    const Footer = (
      <footer className={'row hideable' + (this.state.footerHidden ? ' descended' : '')}>
        <div className='medium-7 columns'>
          <h3>View</h3>
          <ChartSelect
            charts={builderDefinitions.charts}
            value={chart.type}
            onChange={DataExplorerActions.setType}/>
        </div>
        <div className='medium-5 columns'>
          <h3>Color Scheme</h3>
          <PalettePicker
            value={chart.palette}
            onChange={DataExplorerActions.setPalette}/>
          <button className='footer-toggle-button' onClick={this._showHideFooter}>
            <i className={this.state.footerHidden ? 'fa fa-caret-up' : 'fa fa-caret-down'}>&nbsp; </i>
            { this.state.footerHidden ? 'Show' : 'Hide'} Properties
          </button>
        </div>
      </footer>
    )

    // PLACEHOLDERS
    // ---------------------------------------------------------------------------
    let chart_placeholder = <Placeholder height={600}/>
    if (chart.data && chart.data.length === 0) {
      chart_placeholder =  <Placeholder height={600} text='NO DATA' loading={false}/>
    }
    const missingParams = _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)
    if (!chart.data && missingParams) {
      chart_placeholder = <Placeholder height={600} text='Please select an INDICATOR and LOCATION' loading={false}/>
    }

    return (
      <section className='data-explorer'>
        <div className='medium-3 large-2 medium-push-9 large-push-10 columns'>
          { call_to_actions }
          <div className={'row data-filters ' + (multi_indicator && multi_location ? '' : 'collapse')}>
            { date_range_picker }
            { campaign_dropdown }
            { indicator_selector }
            { location_selector }
          </div>
        </div>
        <div className='medium-9 large-10 medium-pull-3 large-pull-2 columns'>
          <div className='row chart-header'>
            { title_bar }
          </div>
          {!_.isEmpty(chart.data) ? chart_component : chart_placeholder}
        </div>
        { Footer }
      </section>
    )
  }
})

export default DataExplorer
