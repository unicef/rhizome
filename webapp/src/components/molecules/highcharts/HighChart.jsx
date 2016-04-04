import _ from 'lodash'
import React, { Component } from 'react'

import LineChartRenderer from 'components/molecules/highcharts/renderers/line-chart'

class HighChart extends Component {

  constructor (props) {
    super(props)
    this.options = props
  }

  componentDidMount () {
    console.info('------ HighChart.componentDidMount')
    this.container = React.findDOMNode(this)
    this.setData()
    this.setOptions()
    if (this.options.type === 'TrendChart') {
      this.chart = new LineChartRenderer(this.data, this.options, this.container)
    }
    this.chart.render()
  }

  componentDidUpdate () {
    console.info('------ HighChart.componentDidUpdate')
    this.options = _.defaults({}, this.props, this.options)
    this.setData()
    this.setOptions()
    this.chart.update(this.data, this.options, this.container)
  }

  setData () {
    console.info('------ HighChart.setData')
    this.data = this.props.data
  }

  setOptions () {
    console.info('------ HighChart.setOptions')
    const aspect = this.options.aspect || 1
    this.options.width = this.props.width || this.container.clientWidth
    this.options.height = this.props.height || this.options.width / aspect
    return this.options
  }

  render () {
    console.info('------ HighChart.render')
    return (
      <div></div>
    )
  }
}

export default HighChart

