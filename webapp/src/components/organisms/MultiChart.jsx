import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import ChartTypeSelector from 'components/molecules/ChartTypeSelector'
import ChartSelector from 'components/molecules/ChartSelector'
import Placeholder from 'components/molecules/Placeholder'

import BarChart from 'components/molecules/highcharts/BarChart'
import MapChart from 'components/molecules/highcharts/MapChart'
import BubbleMap from 'components/molecules/highcharts/BubbleMapChart'
import LineChart from 'components/molecules/highcharts/LineChart'
import ColumnChart from 'components/molecules/highcharts/ColumnChart'
import StackedColumnChart from 'components/molecules/highcharts/StackedColumnChart'
import TableChart from 'components/molecules/charts/TableChart'
import ChoroplethMap from 'components/molecules/charts/ChoroplethMap'
import DatabrowserTable from 'components/molecules/DatabrowserTable'

import MultiChartControls from 'components/organisms/MultiChartControls'
import MultiChartHeader from 'components/organisms/MultiChartHeader'

import ChartStore from 'stores/ChartStore'
import CampaignStore from 'stores/CampaignStore'
import RootStore from 'stores/RootStore'

const MultiChart = React.createClass({

  mixins: [
    Reflux.connect(ChartStore, 'all_charts'),
    Reflux.connect(CampaignStore, 'campaigns'),
  ],

  componentDidMount: function () {
    RootStore.listen(() => {
      if (this.props.chart_id) {
        this.props.fetchChart.completed(this.state.charts.index[this.props.chart_id])
      } else {
        this.props.setCampaigns(this.state.campaigns.raw[0])
      }
    })
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    const missing_params = _.isEmpty(nextProps.chart.selected_indicators) || _.isEmpty(nextProps.chart.selected_locations)
    const chart_data = !_.isEmpty(nextProps.chart.data)
    return chart_data || nextProps.chart.loading || missing_params
  },

  getChartComponentByType: function (type) {
    if (type === 'TableChart') {
      return <TableChart {...this.props.chart} />
    } else if (type === 'LineChart') {
      return <LineChart {...this.props.chart} />
    } else if (type === 'ChoroplethMap') {
      return <ChoroplethMap {...this.props.chart} />
    } else if (type === 'MapChart') {
      return <MapChart {...this.props.chart} />
    } else if (type === 'ColumnChart') {
      return <ColumnChart {...this.props.chart} />
    } else if (type === 'StackedColumnChart') {
      return <StackedColumnChart {...this.props.chart} />
    } else if (type === 'BubbleMap') {
      return <BubbleMap {...this.props.chart} />
    } else if (type === 'BarChart') {
      return <BarChart {...this.props.chart} />
    } else {
      return <DatabrowserTable {...this.props.chart} />
    }
  },

  render: function () { console.info('MultiChart - render '+ this.props.chart.title)
    const chart = this.props.chart

    const chart_selector = (
      <div>
        <br/><h4>or</h4><br/>
        <ChartSelector charts={this.state.all_charts.raw} selectChart={this.props.selectChart} />
      </div>
    )

    const chart_type_selector = (
      <div className='medium-10 medium-centered text-center columns' style={{position: 'relative', marginTop: '-1.5rem', padding: '4rem 0'}}>
        <h4>View Data As</h4>
        <ChartTypeSelector onChange={this.props.setType}/>
        { this.props.selectChart ? chart_selector : null }
      </div>
    )

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

    const sidebar = (
      <aside className='medium-4 large-3 medium-push-8 large-push-9 columns animated slideInRight'>
        <MultiChartControls {...this.props} className='row collapse' />
      </aside>
    )

    const chart_classes = !chart.editMode ? 'medium-12 ' : 'medium-8 large-9 medium-pull-4 large-pull-3 '
    const hideChartFrame = !this.props.readOnlyMode && chart.type === 'RawData'

    return (
      <article className={'multi-chart medium-12 columns' + (!hideChartFrame ? ' no-frame ' : '')}>
        { hideChartFrame ? <MultiChartHeader {...this.props}/> : null }
        <section className='row'>
          { chart.editMode ? sidebar : null }
          <div className={chart_classes + ' columns chart-zone'}>
            {
              chart.selectTypeMode ? chart_type_selector : (
                !_.isEmpty(chart.data) ? this.getChartComponentByType(chart.type) : chart_placeholder
              )
            }
          </div>
        </section>
      </article>
    )
  }
})

export default MultiChart
