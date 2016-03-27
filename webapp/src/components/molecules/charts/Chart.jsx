import _ from 'lodash'
import React, { Component } from 'react'

import LineChartRenderer from 'components/molecules/charts/renderers/line-chart'
import TableChartRenderer from 'components/molecules/charts/renderers/table-chart'
import ChoroplethMapRenderer from 'components/molecules/charts/renderers/choropleth-map'

class Chart extends Component {

  constructor (props) {
    super(props)
    this.params = props
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    const chart = this.getParams()
    if (chart.type === 'LineChart') {
      this.chart = new LineChartRenderer(chart.data, chart, this.container)
    } else if (chart.type === 'TableChart') {
      this.chart = new TableChartRenderer(chart.data, chart, this.container)
    } else if (chart.type === 'ChoroplethMap') {
      this.chart = new ChoroplethMapRenderer(chart.data, chart, this.container)
    }
    this.chart.render()
  }

  componentDidUpdate () {
    this.params = _.defaults({}, this.props, this.params)
    const chart = this.getParams()
    this.chart.update(chart.data, chart, this.container)
  }

  getParams () {
    const aspect = this.params.aspect || 1
    this.params.width = this.props.width || this.container.clientWidth
    this.params.height = this.props.height || this.params.width / aspect
    return this.params
  }

  render () {
    return (
      <svg className='line'>
      </svg>
    )
  }
}

export default Chart

