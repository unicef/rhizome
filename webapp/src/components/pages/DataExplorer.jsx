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
import IndicatorStore from 'stores/IndicatorStore'
import OfficeStore from 'stores/OfficeStore'
import CampaignStore from 'stores/CampaignStore'
import ChartStore from 'stores/ChartStore'
import DatapointStore from 'stores/DatapointStore'

import ChartActions from 'actions/ChartActions'

const DataExplorer = React.createClass({
  mixins: [
    Reflux.connect(ChartStore, 'chart'),
    Reflux.connect(OfficeStore, 'offices'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators'),
    Reflux.connect(DatapointStore, 'datapoints')
  ],

  getInitialState() {
    return {
      footerHidden: false
    }
  },

  propTypes: {
    chart_id: PropTypes.number
  },

  getChart (locations, indicators) {
    if (this.state.locations.index && this.state.indicators.index && this.props.chart_id) {
      ChartActions.fetchChart(this.props.chart_id)
    }
  },

  componentWillMount () {
    LocationStore.listen(this.getChart)
    IndicatorStore.listen(this.getChart)
  },

  componentDidMount () {
    if (this.props.chart_id) { this.setState({footerHidden: true})}
    IndicatorSelectorStore.listen(selected_indicators => {
      return ChartActions.setIndicatorIds(selected_indicators.map(indicator => indicator.id))
    })
    LocationSelectorStore.listen(selected_locations => {
      return ChartActions.setLocationIds(selected_locations.map(location => location.id))
    })
    CampaignStore.listen(campaigns => {
      if (campaigns.raw[0]) {
        ChartActions.setCampaignIds([campaigns.raw[0].id])
      }
    })
  },

  //===========================================================================//
  //                               EVENT HANDLERS                              //
  //===========================================================================//
  _saveChart () {
    const chart_def = this.state.chart.def
    if (!chart_def.title) {
      return window.alert('Please add a Title to your chart')
    }
    ChartActions.postChart({
      id: this.props.chart_id,
      title: chart_def.title,
      chart_json: JSON.stringify({
        type: chart_def.type,
        start_date: chart_def.start_date,
        end_date: chart_def.end_date,
        campaign_ids: chart_def.campaign_ids,
        location_ids: chart_def.location_ids,
        indicator_ids: chart_def.indicator_ids
      })
    })
  },

  _showHideFooter () {
    this.setState({footerHidden: !this.state.footerHidden})
  },

  _toggleTitleEdit (title) {
    console.log('title', title)
    if (_.isString(title)) {
      ChartActions.setTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  //===========================================================================//
  //                                   RENDER                                  //
  //===========================================================================//
  render () {
    const chart = this.state.chart
    const start_date = chart.def ? moment(chart.def.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart.def ? moment(chart.def.end_date, 'YYYY-MM-DD').toDate() : moment()
    const disableSave = _.isEmpty(chart.def.location_ids) || _.isEmpty(chart.def.indicator_ids)
    const preset_indicator_ids = this.props.chart_id && chart ? chart.def.indicator_ids : [15]
    const preset_location_ids = this.props.chart_id && chart ? chart.def.location_ids : [1]
    const multi_indicator = chart.def.type === 'TableChart' || chart.def.type === 'RawData'
    const multi_location = chart.def.type === 'TableChart' || chart.def.type === 'RawData'
    const raw_data_query = {
      format: 'csv',
      indicator__in: chart.def.indicator_ids,
      location__in: chart.def.location_ids,
      campaign_start: start_date,
      campaign_end: end_date
    }
    const campaign_placeholder = <Placeholder height={18}/>
    const chart_placeholder = <Placeholder height={600}/>

    // CHART
    //---------------------------------------------------------------------------
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={chart.def.title} save={this._toggleTitleEdit}/>
      :
      <h1>
        {chart.def.title}
        <a className='button icon-button' onClick={this._toggleTitleEdit}><i className='fa fa-pencil'/></a>
      </h1>

    const chart_component = chart.def.type === 'RawData'?
      <DatabrowserTable
        data={this.state.datapoints.raw}
        selected_locations={chart.def.selected_locations}
        selected_indicators={chart.def.selected_indicators}
      />
      :
      <Chart type={chart.def.type} data={chart.data} options={chart.def} />

    // SIDEBAR
    //---------------------------------------------------------------------------
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

    const date_range_picker = chart.def.type === 'LineChart' ? (
      <div className='medium-12 columns'>
        <h3>Time</h3>
        <DateRangePicker
          sendValue={ChartActions.setDateRange}
          start={start_date}
          end={end_date}
          fromComponent='DataExplorer'
        />
        <br/>
      </div>
    ) : ''

    const campaign_dropdown = chart.def.type !== 'RawData' && chart.def.type !== 'LineChart'?
    (
      <div className='row collapse'>
        <h3>Campaign</h3>
        <CampaignTitleMenu
          campaigns={this.state.campaigns.raw}
          selected={chart.def.selected_campaigns[0]}
          sendValue={ChartActions.setCampaignIds}/>
      </div>
    ) : ''

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
    //---------------------------------------------------------------------------
    const footer = (
      <footer style={{ bottom: this.state.footerHidden ? '-3.4rem' : '3.1rem'}} className='row hideable'>
        <div className='medium-7 columns'>
          <h3>View</h3>
          <ChartSelect
            charts={builderDefinitions.charts}
            value={chart.def.type}
            onChange={ChartActions.setType}/>
        </div>
        <div className='medium-5 columns'>
          <h3>Color Scheme</h3>
          <PalettePicker
            value={chart.def.palette}
            onChange={ChartActions.setPalette}/>
          <button className='footer-toggle-button' onClick={this._showHideFooter}>
            <i className={this.state.footerHidden ? 'fa fa-caret-up' : 'fa fa-caret-down'}>&nbsp; </i>
            { this.state.footerHidden ? 'Show' : 'Hide'} Properties
          </button>
        </div>
      </footer>
    )

    return (
      <section className='data-explorer'>
        <div className='medium-9 large-10 columns'>
          <div className='row chart-header'>
          {!_.isEmpty(chart.def.title) ? title_bar : ''}
          </div>
          {!_.isEmpty(chart.data) ? chart_component : chart_placeholder}
        </div>
        <div className='medium-3 large-2 columns'>
          { call_to_actions }
          <div className={'row data-filters ' + (multi_indicator  && multi_location ? '' : 'collapse')}>
            { date_range_picker }
            {!_.isEmpty(this.state.campaigns.raw) ? campaign_dropdown : campaign_placeholder}
            { indicator_selector }
            { location_selector }
          </div>
        </div>
        { footer }
      </section>
    )
  }
})

export default DataExplorer
