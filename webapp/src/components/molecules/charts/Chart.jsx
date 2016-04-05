import _ from 'lodash'
import React, { Component } from 'react'

import TableChartRenderer from 'components/molecules/charts/renderers/table-chart'
import ChoroplethMapRenderer from 'components/molecules/charts/renderers/choropleth-map'

class Chart extends Component {

  constructor (props) {
    super(props)
    this.options = props
  }

  componentDidMount () {
    console.info('------ Chart.componentDidMount')
    this.container = React.findDOMNode(this)
    this.setData()
    this.setOptions()
    if (this.options.type === 'TableChart') {
      this.chart = new TableChartRenderer(this.data, this.options, this.container)
    } else if (this.options.type === 'ChoroplethMap') {
      this.chart = new ChoroplethMapRenderer(this.data, this.options, this.container)
    }
    this.chart.render()
  }

  componentDidUpdate () {
    console.info('------ Chart.componentDidUpdate')
    this.options = _.defaults({}, this.props, this.options)
    this.setData()
    this.setOptions()
    this.chart.update(this.data, this.options, this.container)
  }

  setData () {
    console.info('------ Chart.setData')
    this.data = this.props.data
  }

  setOptions () {
    console.info('------ Chart.setOptions')
    const aspect = this.options.aspect || 1
    this.options.width = this.props.width || this.container.clientWidth
    this.options.height = this.props.height || this.options.width / aspect
    return this.options
  }

  render () {
    console.info('------ Chart.render')
    return (
      <svg></svg>
    )
  }
}

export default Chart

