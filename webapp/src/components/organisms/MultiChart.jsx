import _ from 'lodash'
import React, {PropTypes} from 'react'
import {DropdownList} from 'react-widgets'
import Reflux from 'reflux'
import moment from 'moment'

import IconButton from 'components/atoms/IconButton'
import ExportIcon from 'components/atoms/ExportIcon'
import ColorSwatch from 'components/atoms/ColorSwatch'
import ChartSelect from 'components/organisms/data-explorer/ChartSelect'

import palettes from 'components/molecules/charts/utils/palettes'
import ChartSelector from 'components/molecules/ChartSelector'
import CampaignSelector from 'components/molecules/CampaignSelector'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import DateRangePicker from 'components/molecules/DateRangePicker'
import Placeholder from 'components/molecules/Placeholder'
import TitleInput from 'components/molecules/TitleInput'
import TableChart from 'components/molecules/charts/TableChart'
import TrendChart from 'components/molecules/highcharts/TrendChart'
import LineChart from 'components/molecules/charts/LineChart'
import ChoroplethMap from 'components/molecules/charts/ChoroplethMap'

import ChartStore from 'stores/ChartStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import RootStore from 'stores/RootStore'

import ChartActions from 'actions/ChartActions'

const MultiChart = React.createClass({
  mixins: [
    Reflux.connect(ChartStore, 'all_charts'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  getInitialState () {
    return {
      titleEditMode: false
    }
  },

  componentDidMount () {
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index && state.charts.index) {
        if (this.props.chart_id) {
          this.props.fetchChart.completed(this.state.charts.index[this.props.chart_id])
        } else {
          this.props.setCampaigns(this.state.campaigns.raw[0])
        }
      }
    })
  },

  shouldComponentUpdate (nextProps, nextState) {
    const missing_params = _.isEmpty(nextProps.chart.selected_indicators) || _.isEmpty(nextProps.chart.selected_locations)
    const chart_data = !_.isEmpty(nextProps.chart.data)
    return chart_data || nextProps.chart.loading || missing_params
  },

  _toggleTitleEdit (title) {
    if (_.isString(title)) {
      this.props.setTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  getChartComponentByType (type) {
    if (type === 'TableChart') {
      return <TableChart {...this.props.chart} />
    } else if (type === 'LineChart') {
      return <LineChart {...this.props.chart} />
    } else if (type === 'ChoroplethMap') {
      return <ChoroplethMap {...this.props.chart} />
    } else if (type === 'ColumnChart') {
      return <TrendChart {...this.props.chart} />
    }
  },

  render () {
    console.info('MultiChart.'+ this.props.chart.title +'.RENDER ==========================================')
    const chart = this.props.chart
    const start_date = chart ? moment(chart.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart ? moment(chart.end_date, 'YYYY-MM-DD').toDate() : moment()
    const disableSave = _.isEmpty(chart.selected_locations) || _.isEmpty(chart.selected_indicators)
    const multi_indicator = chart.type === 'TableChart' || chart.type === 'RawData'
    const multi_location = chart.type === 'TableChart' || chart.type === 'RawData'

    // CHART
    // ---------------------------------------------------------------------------
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={chart.title} save={this._toggleTitleEdit}/>
      :
      <h2>
        <a onClick={this._toggleTitleEdit} style={{cursor: 'text'}}>
          {chart.title || 'Untitled Chart'}
        </a>
      </h2>

    const chart_type_selector = (
      <div className='medium-10 medium-centered text-center columns' style={{position: 'relative', marginTop: '-1.5rem', padding: '4rem 0'}}>
        <h4>View Data As</h4>
        <ChartSelect onChange={this.props.setType}/>
        <br />
        <h4>or</h4>
        <br />
        <ChartSelector charts={this.state.all_charts.raw} selectChart={this.props.selectChart} />
      </div>
    )

    let chart_component = chart.type === 'RawData' ?
      <DatabrowserTable
        data={chart.data}
        selected_locations={chart.selected_locations}
        selected_indicators={chart.selected_indicators}
      />
      : this.getChartComponentByType(chart.type)


    // ACTION ICONS
    // ---------------------------------------------------------------------------
    const change_type_button = (
      <IconButton
        icon='fa-bar-chart'
        text='Change chart type'
        onClick={this.props.toggleSelectTypeMode}
        className='left'
      />
    )
    const export_button = (
      <ExportIcon exportPath={'/charts/' + chart.id}/>
    )
    const duplicate_chart_button = this.props.duplicateChart ? (
      <IconButton
        icon='fa-copy'
        text='Duplicate'
        onClick={() => this.props.duplicateChart(chart.uuid)}
      />
    ) : null
    const save_button = (
      <IconButton
        icon='fa-save'
        text='Save'
        onClick={() => this.props.saveChart(chart.uuid)}
      />
    )
    const remove_chart_button = this.props.removeChart ? (
      <IconButton
        icon='fa-times'
        text='Remove'
        onClick={() => this.props.removeChart(chart.uuid)}
      />
    ) : null

    // SIDEBAR
    // ---------------------------------------------------------------------------
    const date_range_picker = chart.type === 'LineChart' || chart.type === 'RawData' ? (
      <div className='medium-12 columns'>
        <h3>Time</h3>
        <DateRangePicker
          sendValue={this.props.setDateRange}
          start={start_date}
          end={end_date}
          fromComponent='MultiChart'
        />
        <br/>
      </div>
    ) : null

    const campaign_selector = chart.type !== 'LineChart' && chart.type !== 'RawData' ? (
      <CampaignSelector
        campaigns={this.state.campaigns}
        selected_campaigns={chart.selected_campaigns}
        selectCampaign={this.props.selectCampaign}
        deselectCampaign={this.props.deselectCampaign}
        setCampaigns={this.props.setCampaigns}
        linkCampaigns={this.props.linkCampaigns}
        classes='medium-12 columns'
        linked={chart.linkedCampaigns}
      />
    ) : ''

    const location_selector = (
      <LocationSelector
        locations={this.state.locations}
        selected_locations={chart.selected_locations}
        selectLocation={this.props.selectLocation}
        deselectLocation={this.props.deselectLocation}
        setLocations={this.props.setLocations}
        clearSelectedLocations={this.props.clearSelectedLocations}
        classes={multi_location ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multi_location}
      />
    )

    const indicator_selector = (
      <IndicatorSelector
        indicators={this.state.indicators}
        selected_indicators={chart.selected_indicators}
        selectIndicator={this.props.selectIndicator}
        setIndicators={this.props.setIndicators}
        deselectIndicator={this.props.deselectIndicator}
        clearSelectedIndicators={this.props.clearSelectedIndicators}
        reorderIndicator={this.props.reorderIndicator}
        classes={multi_indicator ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multi_indicator}
        avoidBooleans={chart.type === 'LineChart'}
      />
    )

    const palette_selector = chart.type !== 'RawData'  && chart.type !== 'LineChart' ? (
      <div className='medium-12 columns'>
        <h3>Colors</h3>
        <DropdownList
          data={ _.map(palettes, (key, value) => ({colors: key, value: value}) )}
          textField='value'
          valueField='value'
          value={chart.palette}
          itemComponent={ColorSwatch}
          valueComponent={ColorSwatch}
          onChange={item => this.props.setPalette(item.value)}
        />
        <br />
      </div>
    ) : null

    // PLACEHOLDERS
    // ---------------------------------------------------------------------------
    const missing_indicators = _.isEmpty(chart.selected_indicators)
    const missing_locations = _.isEmpty(chart.selected_locations)
    let chart_placeholder = <Placeholder height={300}/>
    if (!chart.loading && (missing_indicators || missing_locations)) {
      let placeholder_text = 'Select a(n) '
      placeholder_text += missing_indicators ? 'INDICATOR ' : ''
      placeholder_text += missing_locations && missing_indicators ? 'and ' : ''
      placeholder_text += missing_locations ? 'LOCATION ' : ''
      chart_placeholder = <Placeholder height={300} text={placeholder_text} loading={false}/>
    } else if (_.isEmpty(chart.data) && !_.isNull(chart.data) && chart.loading) {
      chart_placeholder = <Placeholder height={300} text='NO DATA' loading={false}/>
    }

    return (
      <article className='multi-chart'>
        <header className='row'>
          <div className='medium-4 large-3 medium-push-8 large-push-9 columns text-right chart-actions'>
            <div className='hide-for-medium-up'>
              { change_type_button }
            </div>
            { export_button }
            { duplicate_chart_button }
            { save_button }
            { remove_chart_button }
          </div>
          <div className='medium-8 large-9 medium-pull-4 large-pull-3 columns chart-header text-center'>
            <div className='hide-for-small'>
              { change_type_button }
            </div>
            { title_bar }
          </div>
        </header>
        <section className='row'>
          <aside className='medium-4 large-3 medium-push-8 large-push-9 columns'>
            { palette_selector }
            { date_range_picker }
            { campaign_selector }
            { indicator_selector }
            { location_selector }
          </aside>
          <div className='medium-8 large-9 medium-pull-4 large-pull-3 columns chart-zone'>
            {
              chart.selectTypeMode
                ? chart_type_selector : (!_.isEmpty(chart.data)
                  ? chart_component : chart_placeholder)
            }
          </div>
        </section>
      </article>
    )
  }
})

export default MultiChart
