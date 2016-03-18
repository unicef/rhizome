import _ from 'lodash'
import React, {PropTypes} from 'react'

import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import ChartFactory from 'components/molecules/charts_d3/ChartFactory'
import Placeholder from 'components/molecules/Placeholder'

const D3Chart = React.createClass({

  propTypes: {
    type: PropTypes.string,
    data: PropTypes.arrayOf(
      PropTypes.objectOf({
        id: PropTypes.number
      })
    ).isRequired,
    options: PropTypes.objectOf({
      id: PropTypes.number
    }).isRequired
  },

  getDefaultProps() {
    return {
      type: 'TableChart'
    };
  },

  d3_chart: {},

  d3_legend: {},

  //===========================================================================//
  //                             LIFECYCLE METHODS                             //
  //===========================================================================//
  componentDidMount () {
    this.renderChart(this.props.type, React.findDOMNode(this), this.props.data, this.props.options)
  },

  componentWillReceiveProps (nextProps) {
    if (nextProps.type !== this.props.type) {
      const container = React.findDOMNode(this)
      container.innerHTML = ''
      this.renderChart(nextProps.type, container, nextProps.data, nextProps.options)
    }
  },

  shouldComponentUpdate (nextProps, nextState) {
    return nextProps.data !== this.props.data
  },

  componentDidUpdate () {
    this.chart.update(this.props.data, this.props.options, React.findDOMNode(this))
  },

  //===========================================================================//
  //                                  RENDER                                   //
  //===========================================================================//
  renderChart (type, container, data, options) {
    this.setState({placeholder_text})
    this.d3_chart = ChartFactory(type, container, data, options)
    if (type ===' ChoroplethMap') {
      this.d3_legend = ChartFactory('ChoroplethMapLegend', container, data, options)
    }
  },

  render () {
    const props = this.props
    const type = props.type
    const chart_key = props.id ? 'chart-' + props.id : 'chart-' + type
    const placeholder = <Placeholder height='360' text='' />
    const chart = <div ref={chart_key + '-component'} className={'chart ' + _.kebabCase(type)}></div>
    const legend = <div ref={chart_key + '-legend'} className='chart choropleth-map-legend'></div>
    const chart_component = type === 'ChoroplethMap' ? [chart, legend] : chart
    return (
      <div className='chart-container'>
        { type === 'RawData' ? placeholder : chart_component }
      </div>
    )
  }
})

export default D3Chart
