import _ from 'lodash'
import React, { Component } from 'react'

import LineChartRenderer from 'components/molecules/charts/renderers/line-chart'
import TableChartRenderer from 'components/molecules/charts/renderers/table-chart'
import ChoroplethMapRenderer from 'components/molecules/charts/renderers/choropleth-map'

class Chart extends Component {

  constructor (props) {
    super(props)
    this.options = props
    this.data = props.data
  }

  componentDidMount () {
    console.log('------ Chart.componentDidMount')
    this.container = React.findDOMNode(this)
    const options = this.setOptions()
    if (options.type === 'LineChart') {
      this.chart = new LineChartRenderer(this.data, this.options, this.container)
    } else if (options.type === 'TableChart') {
      this.chart = new TableChartRenderer(this.data, this.options, this.container)
    } else if (options.type === 'ChoroplethMap') {
      this.chart = new ChoroplethMapRenderer(this.data, this.options, this.container)
    }
    this.chart.render()
  }

  componentDidUpdate () {
    console.log('------ Chart.componentDidUpdate')
    this.options = _.defaults({}, this.props, this.options)
    const chart = this.setOptions()
    this.chart.update(this.data, this.options, this.container)
  }

  setOptions () {
    console.log('------ Chart.setOptions')
    const aspect = this.options.aspect || 1
    this.options.width = this.props.width || this.container.clientWidth
    this.options.height = this.props.height || this.options.width / aspect
    return this.options
  }

  render () {
    console.log('------ Chart.render')
    return (
      <svg></svg>
    )
  }
}

export default Chart

