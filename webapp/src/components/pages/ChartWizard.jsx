import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import DropdownList from 'react-widgets/lib/DropdownList'
import DateRangePicker from 'components/molecules/DateRangePicker'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'
import TitleInput from 'components/molecules/TitleInput'


import Placeholder from 'components/molecules/Placeholder'
import ChartInfo from 'components/molecules/charts_d3/ChartInfo'
import ChartInit from 'components/molecules/charts_d3/ChartInit'
import Chart from 'components/molecules/Chart'
import DownloadButton from 'components/molecules/DownloadButton'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import PreviewScreen from 'components/organisms/chart-wizard/PreviewScreen'
import ChartSelect from 'components/organisms/chart-wizard/ChartSelect'
import PalettePicker from 'components/organisms/chart-wizard/preview/PalettePicker'

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
import builderDefinitions from 'components/molecules/charts_d3/utils/builderDefinitions'

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
    CampaignStore.listen(campaigns => {
      if (campaigns.raw[0]) {
        ChartActions.setCampaignIds([campaigns.raw[0].id])
      }
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

    const chart_component = chart.def.type === 'RawData'
      ? <DatabrowserTable
          data={this.state.datapoints.raw}
          selected_locations={chart.def.selected_locations}
          selected_indicators={chart.def.selected_indicators}
        />
      : <Chart type={chart.def.type} data={chart.data} options={chart.def} />

    const sidebar_component = (
      <div>
        <div className='row collapse'>
          <div className='medium-12 large-5 large-push-7 columns'>
            <button className='expand button success field-submit' disabled={!chart.data} onClick={ChartActions.saveChart}>
              <i className='fa fa-save'></i> Save To Charts
            </button>
          </div>
          <div className='medium-12 large-7 large-pull-5 columns'>
            <h3>Chart Title</h3>
            <TitleInput initialText={chart.def.title} save={ChartActions.setTitle}/>
          </div>
        </div>
        <div className='row'>
          <h3>Time</h3>
          <DateRangePicker
            sendValue={ChartActions.setDateRange}
            start={start_date}
            end={end_date}
            fromComponent='ChartWizard'
          />
          <br/>
        </div>
        {
          chart.def.type !== 'RawData' ?
          (
            <div className='row collapse'>
              <h3>Campaign</h3>
              <DropdownList
                data={this.state.campaigns.raw}
                defaultValue={this.state.campaigns.raw ? this.state.campaigns.raw[0].id : null}
                textField='name'
                valueField='id'
                disabled={chart.def.type === 'RawData'}
                onChange={campaign => ChartActions.setCampaignIds([campaign.id])}
              />
            </div>
          ) : ''
        }
        <div className='row data-filters'>
          <br/>
          <IndicatorSelector
            indicators={this.state.indicators}
            preset_indicator_ids={[31, 29, 26]}
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

    const sidebar_placeholder = <Placeholder height='200'/>
    const chart_placeholder =  <Placeholder height='600'/>

    return (
      <section className='chart-wizard'>
        <div className='medium-9 columns'>
          {!_.isEmpty(chart.data) ? chart_component : chart_placeholder}
        </div>
        <div className='medium-3 columns'>
          {this.initDataReady() ? sidebar_component : sidebar_placeholder}
        </div>
        <footer className='row'>
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
          </div>
        </footer>
      </section>
    )
  }
})

export default ChartWizard
