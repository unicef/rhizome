import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import DashboardChartsStore from 'stores/DashboardChartsStore'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import MultiChart from 'components/organisms/MultiChart'

const DashboardRow = React.createClass({

  mixins: [
    Reflux.connect(DashboardChartsStore, 'charts'),
  ],

  propTypes: {
    charts: PropTypes.array,
    layout: PropTypes.number,
    editMode: PropTypes.bool,
    rowIndex: PropTypes.number,
    selectRowLayout: PropTypes.func
  },

  getDefaultProps: function () {
    return {
      rowIndex: null,
      charts: null,
      layout: null
    }
  },

  renderChart: function (chart, chart_index) { console.info('DashboardRow - renderChart')
    return (
      <MultiChart
        chart={chart}
        readOnlyMode={!this.props.editMode}
        linkCampaigns={() => DashboardChartsActions.toggleCampaignLink(chart.uuid)}
        duplicateChart={DashboardChartsActions.duplicateChart}
        selectChart={new_chart => DashboardChartsActions.selectChart(new_chart, chart.uuid)}
        toggleSelectTypeMode={() => DashboardChartsActions.toggleSelectTypeMode(chart.uuid)}
        toggleEditMode={() => DashboardChartsActions.toggleChartEditMode(chart.uuid)}
        removeChart={() => DashboardPageActions.removeChart(this.props.rowIndex, chart_index)}
        saveChart={() => DashboardChartsActions.saveChart(chart.uuid)}
        setDateRange={(key, value) => DashboardChartsActions.setDateRange(key, value, chart.uuid)}
        setGroupBy={(grouping) => DashboardChartsActions.setGroupBy(grouping, chart.uuid)}
        setPalette={(palette) => DashboardChartsActions.setPalette(palette, chart.uuid)}
        setTitle={(title) => DashboardChartsActions.setChartTitle(title, chart.uuid)}
        setType={(type) => DashboardChartsActions.setType(type, chart.uuid)}
        setIndicators={(indicators) => DashboardChartsActions.setIndicators(indicators, chart.uuid)}
        selectIndicator={(id) => DashboardChartsActions.selectIndicator(id, chart.uuid)}
        deselectIndicator={(id) => DashboardChartsActions.deselectIndicator(id, chart.uuid)}
        reorderIndicator={(indicators) => DashboardChartsActions.reorderIndicator(indicators, chart.uuid)}
        clearSelectedIndicators={() => DashboardChartsActions.clearSelectedIndicators(chart.uuid)}
        setLocations={(locations) => DashboardChartsActions.setLocations(locations, chart.uuid)}
        selectLocation={(id) => DashboardChartsActions.selectLocation(id, chart.uuid)}
        deselectLocation={(id) => DashboardChartsActions.deselectLocation(id, chart.uuid)}
        clearSelectedLocations={() => DashboardChartsActions.clearSelectedLocations(chart.uuid)}
        setCampaigns={(campaigns) => DashboardChartsActions.setCampaigns(campaigns, chart.uuid)}
        selectCampaign={(id) => DashboardChartsActions.selectCampaign(id, chart.uuid)}
        deselectCampaign={(id) => DashboardChartsActions.deselectCampaign(id, chart.uuid)}
      />
    )
  },

  renderRow: function (layout, uuids) {
    const chart_slot = <div className='chart-preview'></div>
    const charts = this.state.charts
    if (layout === 2) {
      return (
        <div className='row animated fadeInDown'>
          <div className='medium-6 columns'>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
          <div className='medium-6 columns'>{uuids ? this.renderChart(charts[uuids[1]], 1) : chart_slot}</div>
        </div>
      )
    } else if (layout === 3) {
      return (
        <div className='row animated fadeInDown'>
          <div className='medium-4 columns'>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
          <div className='medium-4 columns'>{uuids ? this.renderChart(charts[uuids[1]], 1) : chart_slot}</div>
          <div className='medium-4 columns'>{uuids ? this.renderChart(charts[uuids[2]], 2) : chart_slot}</div>
        </div>
      )
    } else if (layout === 4) {
      return (
        <div className='row animated fadeInDown' style={{display: 'flex'}}>
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
        <div className='medium-12 columns'>{uuids ? this.renderChart(charts[uuids[0]], 0) : chart_slot}</div>
      </div>
    )
  },

  render: function () {
    const props = this.props
    const layouts = [1,2,3,4]

    const layout_options = layouts.map(layout =>
      <button className='layout-preview' onClick={() => DashboardPageActions.selectRowLayout(layout)}>
       { this.renderRow(layout) }
      </button>
    )

    const layout_selector = (
      <div className='row layout-options text-center'>
        <h4 className='medium-12 columns'>{'Select chart layout for this row'}</h4>
        <div className='clearfix'></div>
        { layout_options }
      </div>
    )

    return !props.layout ? layout_selector : this.renderRow(props.layout, props.charts)
  }
})

export default DashboardRow
