import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import ChartTypeSelector from 'components/molecules/ChartTypeSelector'
import ChartSelector from 'components/molecules/ChartSelector'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import Placeholder from 'components/molecules/Placeholder'
import TableChart from 'components/molecules/charts/TableChart'
import BarChart from 'components/molecules/highcharts/BarChart'
import ColumnChart from 'components/molecules/highcharts/ColumnChart'
import TrendChart from 'components/molecules/highcharts/TrendChart'
import MapChart from 'components/molecules/highcharts/MapChart'
import ChoroplethMap from 'components/molecules/charts/ChoroplethMap'

import MultiChartControls from 'components/organisms/MultiChartControls'
import MultiChartHeader from 'components/organisms/MultiChartHeader'

import ChartStore from 'stores/ChartStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import RootStore from 'stores/RootStore'

const MultiChart = React.createClass({

  mixins: [
    Reflux.connect(ChartStore, 'all_charts'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

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

  getChartComponentByType (type) {
    if (type === 'TableChart') {
      return <TableChart {...this.props.chart} />
    } else if (type === 'LineChart') {
      return <TrendChart {...this.props.chart} />
    } else if (type === 'ChoroplethMap') {
      return <ChoroplethMap {...this.props.chart} />
    } else if (type === 'MapChart') {
      return <MapChart {...this.props.chart} />
    } else if (type === 'ColumnChart') {
      return <ColumnChart {...this.props.chart} />
    } else if (type === 'BarChart') {
      return <BarChart {...this.props.chart} />
    }
  },

  render () {
    console.info('MultiChart.'+ this.props.chart.title +'.RENDER ==========================================')
    const props = this.props
    const chart = props.chart

    // CHART
    // ---------------------------------------------------------------------------
    const chart_type_selector = (
      <div className='medium-10 medium-centered text-center columns' style={{position: 'relative', marginTop: '-1.5rem', padding: '4rem 0'}}>
        <h4>View Data As</h4>
        <ChartTypeSelector onChange={props.setType}/>
        <br />
        <h4>or</h4>
        <br />
        <ChartSelector charts={this.state.all_charts.raw} selectChart={props.selectChart} />
      </div>
    )

    let chart_component = chart.type === 'RawData' ?
      <DatabrowserTable
        data={chart.data}
        selected_locations={chart.selected_locations}
        selected_indicators={chart.selected_indicators}
      />
      : this.getChartComponentByType(chart.type)

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
        <MultiChartHeader {...props}/>
        <section className='row'>
          <MultiChartControls {...props} className='medium-4 large-3 medium-push-8 large-push-9 columns' />
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
