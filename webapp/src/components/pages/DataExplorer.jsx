import _ from 'lodash'
import api from 'data/api'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import DropdownList from 'react-widgets/lib/DropdownList'

import PalettePicker from 'components/organisms/data-explorer/preview/PalettePicker'
import ChartSelect from 'components/organisms/data-explorer/ChartSelect'

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

  componentWillMount () {
    LocationStore.listen(this.getChart)
    IndicatorStore.listen(this.getChart)
  },

  getChart (locations, indicators) {
    if (this.state.locations.index && this.state.indicators.index && this.props.chart_id) {
      ChartActions.fetchChart(this.props.chart_id)
    }
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

  showHideFooter () {
    this.setState({footerHidden: !this.state.footerHidden})
  },

  render () {
    const chart = this.state.chart
    const start_date = chart.def ? moment(chart.def.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart.def ? moment(chart.def.end_date, 'YYYY-MM-DD').toDate() : moment()
    const disableSave = _.isEmpty(chart.def.location_ids) || _.isEmpty(chart.def.indicator_ids)
    const raw_data_query = {
      format: 'csv',
      indicator__in: chart.def.indicator_ids,
      location__in: chart.def.location_ids,
      campaign_start: start_date,
      campaign_end: end_date
    }
    const campaign_placeholder = <Placeholder height={18}/>
    const chart_placeholder = <Placeholder height={600}/>

    const campaign_dropdown = chart.def.type !== 'RawData' && chart.def.type !== 'LineChart'?
    (
      <div className='row collapse'>
        <h3>Campaign</h3>
        <DropdownList
          data={this.state.campaigns.raw}
          defaultValue={!_.isEmpty(this.state.campaigns.raw) ? this.state.campaigns.raw[0].id : null}
          textField='name'
          valueField='id'
          disabled={chart.def.type === 'RawData'}
          onChange={campaign => ChartActions.setCampaignIds([campaign.id])}
        />
      </div>
    ) : ''

    const date_range_picker = chart.def.type === 'LineChart' ? (
      <div className='row'>
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

    const chart_component = chart.def.type === 'RawData'
      ? <DatabrowserTable
          data={this.state.datapoints.raw}
          selected_locations={chart.def.selected_locations}
          selected_indicators={chart.def.selected_indicators}
        />
      : <Chart type={chart.def.type} data={chart.data} options={chart.def} />

    const preset_indicator_ids = this.props.chart_id && this.state.chart ? this.state.chart.def.indicator_ids : [15]
    const preset_location_ids = this.props.chart_id && this.state.chart ? this.state.chart.def.location_ids : [1]
    const multi_indicator = chart.def.type === 'TableChart'
    const multi_location = chart.def.type === 'TableChart'
    return (
      <section className='data-explorer'>
        <div className='medium-9 columns'>
          {!_.isEmpty(chart.data) ? chart_component : chart_placeholder}
        </div>
        <div className='medium-3 columns'>
          <div className='row collapse'>
            <ExportPdf className='export-file' />
            <DownloadButton
              onClick={() => api.datapoints.toString(raw_data_query)}
              enable={this.state.datapoints.raw}
              text='Download Data'
              working='Downloading'
              cookieName='dataBrowserCsvDownload'/>
            <div className='medium-12 large-5 large-push-7 columns'>
            <button className='expand button success field-submit' disabled={disableSave} onClick={this._saveChart}>
              <i className='fa fa-save'></i> {this.props.chart_id ? 'Save Chart' : 'Save To Charts'}
            </button>
            </div>
            <div className='medium-12 large-7 large-pull-5 columns'>
              <h3>Title</h3>
              <TitleInput initialText={chart.def.title} save={ChartActions.setTitle}/>
            </div>
          </div>
          { date_range_picker }
          {!_.isEmpty(this.state.campaigns.raw) ? campaign_dropdown : campaign_placeholder}
          <div className={'row data-filters ' + (multi_indicator  && multi_location ? '' : 'collapse')}>
            <br/>
            <IndicatorSelector
              indicators={this.state.indicators}
              preset_indicator_ids={preset_indicator_ids}
              classes={multi_indicator ? 'medium-6 columns' : 'medium-12 columns'}
              multi={multi_indicator}
            />
            {multi_indicator && multi_location ? '' : <br/>}
            <LocationSelector
              locations={this.state.locations}
              preset_location_ids={preset_location_ids}
              classes={multi_location ? 'medium-6 columns' : 'medium-12 columns'}
              multi={multi_location}
            />
          </div>
        </div>
        <footer style={{ bottom: this.state.footerHidden ? '-3.4rem' : '3.1rem'}} className='row hideable'>
          <div className='medium-7 columns'>
            <h3>Chart Type</h3>
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
            <button className='footer-toggle-button' onClick={this.showHideFooter}>
              <i className={this.state.footerHidden ? 'fa fa-caret-up' : 'fa fa-caret-down'}>&nbsp; </i>
              { this.state.footerHidden ? 'Show' : 'Hide'} Properties
            </button>
          </div>
        </footer>
      </section>
    )
  }
})

export default DataExplorer
