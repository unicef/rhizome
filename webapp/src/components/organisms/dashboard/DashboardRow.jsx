import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import DashboardContainerActions from 'actions/DashboardContainerActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import IconButton from 'components/button/IconButton'
import MultiChart from 'components/organisms/multi-chart/MultiChart'

const DashboardRow = React.createClass({

  propTypes: {
    all_charts: PropTypes.object,
    charts: PropTypes.array,
    layout: PropTypes.number,
    editMode: PropTypes.bool,
    rowIndex: PropTypes.number,
    selectRowLayout: PropTypes.func
  },

  getDefaultProps: function () {
    return {
      rowIndex: null,
      all_charts: null,
      charts: null,
      layout: null
    }
  },

  onChartClick: function (value, chart) {
    const selected_location_type = chart.selected_locations[0].location_type_id
    if (chart.type === 'MapChart' && selected_location_type < 2) {
      DashboardContainerActions.setLocation(value, chart.uuid)
    }
  },

  renderChart: function (chart, chart_index) {
    return (
      <MultiChart
        chart={chart}
        readOnlyMode={!this.props.editMode}
        primaryChartClick={value => this.onChartClick(value, chart)}
        linkCampaigns={() => DashboardChartsActions.toggleCampaignLink(chart.uuid)}
        duplicateChart={DashboardChartsActions.duplicateChart}
        selectChart={new_chart => DashboardContainerActions.selectChart(new_chart, chart.uuid, this.props.rowIndex, chart_index)}
        toggleSelectTypeMode={() => DashboardChartsActions.toggleSelectTypeMode(chart.uuid)}
        toggleEditMode={() => DashboardChartsActions.toggleChartEditMode(chart.uuid)}
        removeChart={() => DashboardContainerActions.removeChart(this.props.rowIndex, chart_index)}
        saveChart={() => DashboardChartsActions.saveChart(chart.uuid)}
        updateTypeParams={(key, value) => DashboardChartsActions.updateTypeParams(key, value, chart.uuid)}
        setDateRange={(key, value) => DashboardChartsActions.setDateRange(key, value, chart.uuid)}
        setGroupBy={grouping => DashboardChartsActions.setGroupBy(grouping, chart.uuid)}
        setGroupByTime={grouping => DashboardChartsActions.setGroupByTime(grouping, chart.uuid)}
        setPalette={palette => DashboardChartsActions.setPalette(palette, chart.uuid)}
        setTitle={title => DashboardChartsActions.setChartTitle(title, chart.uuid)}
        setType={type => DashboardChartsActions.setType(type, chart.uuid)}
        setIndicators={indicators => DashboardChartsActions.setIndicators(indicators, chart.uuid)}
        setIndicatorFilter={filter => DashboardChartsActions.setIndicatorFilter(filter, chart.uuid)}
        setIndicatorColor={(indicator, color) => DashboardChartsActions.setIndicatorColor(indicator, color, chart.uuid)}
        selectIndicator={id => DashboardChartsActions.selectIndicator(id, chart.uuid)}
        deselectIndicator={id => DashboardChartsActions.deselectIndicator(id, chart.uuid)}
        reorderIndicator={indicators => DashboardChartsActions.reorderIndicator(indicators, chart.uuid)}
        clearSelectedIndicators={() => DashboardChartsActions.clearSelectedIndicators(chart.uuid)}
        setLocationDepth={depth => DashboardChartsActions.setLocationDepth(depth, chart.uuid)}
        setLocations={locations => DashboardChartsActions.setLocations(locations, chart.uuid)}
        selectLocation={id => DashboardChartsActions.selectLocation(id, chart.uuid)}
        deselectLocation={id => DashboardChartsActions.deselectLocation(id, chart.uuid)}
        clearSelectedLocations={() => DashboardChartsActions.clearSelectedLocations(chart.uuid)}
        setCampaigns={campaigns => DashboardChartsActions.setCampaigns(campaigns, chart.uuid)}
        selectCampaign={id => DashboardChartsActions.selectCampaign(id, chart.uuid)}
        deselectCampaign={id => DashboardChartsActions.deselectCampaign(id, chart.uuid)}
      />
    )
  },

  renderRow: function (layout, uuids) {
    const rowIndex = this.props.rowIndex
    const chart_slot = <div className='chart-preview'></div>
    const charts = this.props.all_charts
    const row_order_buttons = this.props.editMode && uuids ? (
      <div className='row-position-buttons'>
        {
          rowIndex !== 0
          ? <IconButton onClick={() => DashboardContainerActions.moveRowUp(rowIndex)} icon='fa-arrow-up' />
          : null
        }
        {
          rowIndex !== this.props.totalRows - 1
          ? <IconButton onClick={() => DashboardContainerActions.moveRowDown(rowIndex)} icon='fa-arrow-down' />
          : null
        }
      </div>
    ) : null

    if (layout === 2) {
      return (
        <div className='row animated fadeInDown'>
          {row_order_buttons}
          <div className='medium-6 columns'>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
          <div className='medium-6 columns'>{uuids ? this.renderChart(charts[uuids[1]], 1) : chart_slot}</div>
        </div>
      )
    } else if (layout === 3) {
      return (
        <div className='row animated fadeInDown'>
          {row_order_buttons}
          <div className='medium-4 columns'>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
          <div className='medium-4 columns'>{uuids ? this.renderChart(charts[uuids[1]], 1) : chart_slot}</div>
          <div className='medium-4 columns'>{uuids ? this.renderChart(charts[uuids[2]], 2) : chart_slot}</div>
        </div>
      )
    } else if (layout === 4) {
      return (
        <div className='row animated fadeInDown' style={{display: 'flex'}}>
          {row_order_buttons}
          <div className='medium-6 columns' style={{display: 'flex'}}>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
          <div className='medium-6 columns'>
            <div className='row'>
              <div className='medium-12 columns'>{uuids ? this.renderChart(charts[uuids[1]], 1) : chart_slot}</div>
            </div>
            <div className='row'>
              <div className='medium-12 columns'>{uuids ? this.renderChart(charts[uuids[2]], 2) : chart_slot}</div>
            </div>
          </div>
        </div>
      )
    }
    return (
      <div className='row animated fadeInDown'>
        {row_order_buttons}
        <div className='medium-12 columns'>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
      </div>
    )
  },

  render: function () {
    const props = this.props
    const layouts = [1,2,3,4]

    if (!_.isEmpty(props.charts)) {
      return this.renderRow(props.layout, props.charts)
    }

    const layout_options = layouts.map(layout =>
      <button className='layout-preview' onClick={() => DashboardContainerActions.selectRowLayout(layout)}>
       { this.renderRow(layout) }
      </button>
    )

    return (
      <div className='row layout-options text-center'>
        <h4 className='medium-12 columns'>{'Select chart layout for this row'}</h4>
        <div className='clearfix'></div>
        { layout_options }
      </div>
    )
  }
})

export default DashboardRow
