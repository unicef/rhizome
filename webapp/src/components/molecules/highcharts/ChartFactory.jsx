import _ from 'lodash'
import React, { Component, PropTypes } from 'react'
import format from 'utilities/format'

import Highcharts from 'highcharts'
import Exporting from 'highcharts/modules/exporting'
import Map from 'highcharts/modules/map'
Exporting(Highcharts)
Map(Highcharts)

class ChartFactory extends Component {
  constructor (props) {
    super(props)
  }

  propTypes: {
    config: React.PropTypes.object.isRequired,
    map: React.PropTypes.bool,
    isPureConfig: React.PropTypes.bool,
    neverReflow: React.PropTypes.bool
  }

  renderChart (config) { console.info('ChartFactory - renderChart')
    let chartConfig = config.chart
    const chartType = this.props.map ? 'Map' : 'Chart'
    this.chart = new Highcharts[chartType]({
      ...config,
      chart: {
        ...chartConfig,
        renderTo: this.refs.chart.getDOMNode()
      }
    })

    global.requestAnimationFrame && requestAnimationFrame(()=>{
      this.chart && this.chart.options && this.chart.reflow()
    })
  }

  shouldComponentUpdate(nextProps) { console.info('ChartFactory - shouldComponentUpdate')
    if (this.props.neverReflow || (this.props.isPureConfig  && this.props.config === nextProps.config)) {
      return true
    }
    this.renderChart(nextProps.config)
    return false
  }

  getChart () { console.info('ChartFactory - getChart')
    if (!this.chart) {
      throw new Error('getChart() should not be called before the component is mounted')
    }
    return this.chart
  }

  componentDidMount () { console.info('ChartFactory - componentDidMount')
    this.renderChart(this.props.config)
  }

  componentWillUnmount() { console.info('ChartFactory - componentWillUnmount')
    this.chart.destroy()
  }

  render () { console.info('ChartFactory - renderChart')
    let props = this.props
    props = {
      ...props,
      ref: 'chart'
    }
    return <div {...props} />
  }
}

export default ChartFactory

