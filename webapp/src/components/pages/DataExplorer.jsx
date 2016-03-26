import _ from 'lodash'
import api from 'data/api'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import PalettePicker from 'components/organisms/data-explorer/preview/PalettePicker'
import ChartSelect from 'components/organisms/data-explorer/ChartSelect'

import builderDefinitions from 'components/molecules/charts/utils/builderDefinitions'
import ExportPdf from 'components/molecules/ExportPdf'
import CampaignSelector from 'components/molecules/CampaignSelector'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import DownloadButton from 'components/molecules/DownloadButton'
import DateRangePicker from 'components/molecules/DateRangePicker'
import Placeholder from 'components/molecules/Placeholder'
import TitleInput from 'components/molecules/TitleInput'

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
    console.info('DataExplorer.getInitialState')
    return {
      footerHidden: false,
      titleEditMode: false
    }
  },

  propTypes: {
    chart_id: PropTypes.number
  },

  componentDidMount () {
    console.info('DataExplorer.componentDidMount')
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index &&  state.campaigns.index && state.charts.index) {
        if (this.props.chart_id) {
          DataExplorerActions.fetchChart.completed(this.state.charts.index[this.props.chart_id])
        } else {
          DataExplorerActions.setIndicators(this.state.indicators.index[27])
          DataExplorerActions.setLocations(this.state.locations.index[1])
          DataExplorerActions.setCampaigns(this.state.campaigns.raw[0])
        }
      }
    })
    if (this.props.chart_id) { this.setState({footerHidden: true}) }
  },

  shouldComponentUpdate(nextProps, nextState) {
    const missing_params = _.isEmpty(nextState.chart.selected_indicators) || _.isEmpty(nextState.chart.selected_locations)
    const chart_data = !_.isEmpty(nextState.chart.data)
    return chart_data
  },

  // =========================================================================== //
  //                                EVENT HANDLERS                               //
  // =========================================================================== //
  _saveChart () {
    console.info('DataExplorer._saveChart')
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
    console.info('DataExplorer._showHideFooter')
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
  getChartComponentByType (type) {
    if (type === 'TableChart') {
      return <TableChart {...this.state.chart} />
    } else if (type === 'LineChart') {
      return <LineChart {...this.state.chart} />
    } else if (type === 'ChoroplethMap') {
      return <ChoroplethMap {...this.state.chart} />
    }
  },

  render () {
    console.info('DataExplorer.RENDER ==========================================')
    const chart = this.state.chart
    const start_date = chart ? moment(chart.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart ? moment(chart.end_date, 'YYYY-MM-DD').toDate() : moment()
    const disableSave = _.isEmpty(chart.selected_locations) || _.isEmpty(chart.selected_indicators)
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
        data={chart.data}
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

    const date_range_picker = chart.type === 'LineChart' || chart.type === 'TableChart' ? (
      <div className=''>
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

    const campaign_selector = chart.type !== 'LineChart' ? (
      <CampaignSelector
        campaigns={this.state.campaigns}
        selected_campaigns={chart.selected_campaigns}
        selectCampaign={DataExplorerActions.selectCampaign}
        deselectCampaign={DataExplorerActions.deselectCampaign}
        setCampaigns={DataExplorerActions.setCampaigns}
      />
    ) : ''

    const location_selector = (
      <LocationSelector
        locations={this.state.locations}
        selected_locations={chart.selected_locations}
        selectLocation={DataExplorerActions.selectLocation}
        deselectLocation={DataExplorerActions.deselectLocation}
        setLocations={DataExplorerActions.setLocations}
        classes={multi_location ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multi_location}
      />
    )

    const indicator_selector = (
      <IndicatorSelector
        indicators={this.state.indicators}
        selected_indicators={chart.selected_indicators}
        selectIndicator={DataExplorerActions.selectIndicator}
        setIndicators={DataExplorerActions.setIndicators}
        deselectIndicator={DataExplorerActions.deselectIndicator}
        clearSelectedIndicators={DataExplorerActions.clearSelectedIndicators}
        reorderIndicator={DataExplorerActions.reorderIndicator}
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
      chart_placeholder = <Placeholder height={600} text='NO DATA' loading={false}/>
    }
    const missingParams = _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)
    if (!chart.data && missingParams) {
      chart_placeholder = <Placeholder height={600} text='Please select an INDICATOR and LOCATION' loading={false}/>
    }

    return (
      <section className='data-explorer'>
        <div className='medium-3 large-2 medium-push-9 large-push-10 columns'>
            { call_to_actions }
            { date_range_picker }
            { campaign_selector }
          <div className={'row data-filters ' + (multi_indicator && multi_location ? '' : 'collapse')}>
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
