import _ from 'lodash'
import React from 'react'

import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import ChartFactory from 'components/molecules/charts_d3/ChartFactory'
import Placeholder from 'components/molecules/Placeholder'

const D3Chart = React.createClass({

  propTypes: {
    data: React.PropTypes.array.isRequired,
    def: React.PropTypes.object.isRequired
  },

  d3_chart: {},

  d3_legend: {},

  componentDidMount () {
    renderChart(this.props.type, React.findDOMNode(this), this.props.data, this.props.options)
  },

  componentWillReceiveProps (nextProps) {
    if (nextProps.type !== this.props.type) {
      const container = React.findDOMNode(this)
      container.innerHTML = ''
      renderChart(nextProps.type, container, nextProps.data, nextProps.options)
    }
  },

  shouldComponentUpdate (nextProps, nextState) {
    return nextProps.data !== this.props.data
  },

  componentDidUpdate () {
    this.chart.update(this.props.data, this.props.options, React.findDOMNode(this))
  },

  renderChart (type, container, data, options) {
    this.d3_chart = ChartFactory(type, container, data, options)
    if (type ===' ChoroplethMap') {
      this.d3_legend = ChartFactory('ChoroplethMapLegend', container, data, options)
    }
  },

  render () {
    const chart = this.props.chart
    const type = chart.type
    const chart_key = chart.id ? 'chart-' + chart.id : 'chart-' + type

    const chart_component = <div ref={chart_key + '-component'} className={'chart ' + _.kebabCase(type)}></div>
    const chart_legend = <div ref={chart_key +'-legend'} className='chart choropleth-map-legend'></div>

    return (
      <div className='chart-container'>
        { chart_component }
        { type === 'ChoroplethMap' ? chart_legend }
      </div>
    )
  }
})

export default D3Chart
