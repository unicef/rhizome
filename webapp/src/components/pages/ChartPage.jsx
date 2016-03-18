import React from 'react'
import Reflux from 'reflux'

import Chart from 'components/molecules/Chart'
import ExportPdf from 'components/molecules/ExportPdf'
import DatabrowserTable from 'components/molecules/DatabrowserTable'

import RootStore from 'stores/RootStore'
import IndicatorStore from 'stores/IndicatorStore'
import LocationStore from 'stores/LocationStore'
import ChartStore from 'stores/ChartStore'
import DatapointStore from 'stores/DatapointStore'
import ChartActions from 'actions/ChartActions'

var ChartPage = React.createClass({

  mixins: [
    Reflux.ListenerMixin,
    Reflux.connect(ChartStore, 'chart'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(IndicatorStore, 'indicators'),
    Reflux.connect(DatapointStore, 'datapoints')
  ],

  propTypes: {
    chart_id: React.PropTypes.number
  },

  componentWillMount () {
    Reflux.connect(LocationStore, 'chart')
    LocationStore.listen(this.getChart)
  },

  getChart (locations, indicators) {
    if (this.state.locations.index && this.state.indicators.index) {
      ChartActions.fetchChart(this.props.chart_id)
    }
  },

  render () {
    const chart = this.state.chart
    const chart_component = chart.def.type === 'RawData'
      ? <DatabrowserTable
          data={this.state.datapoints.raw}
          selected_locations={chart.def.selected_locations}
          selected_indicators={chart.def.selected_indicators}
        />
      : <Chart type={chart.def.type} data={chart.data} options={chart.def} />

    return (
      <div className='row layout-basic'>
        <div className='medium-12 columns text-center'>
          <h1>{ chart.def.title }</h1>
        </div>
        <div className='medium-2 columns'>
          <a href={'/charts/' + this.props.chart_id + '/edit'} className='button expand small'>
            <i className='fa fa-pencil'></i> Edit Chart
          </a>
          <ExportPdf className='button expand small' />
        </div>
        <div className='medium-10 columns'>
          {chart_component}
        </div>
      </div>
    )
  }
})

export default ChartPage
