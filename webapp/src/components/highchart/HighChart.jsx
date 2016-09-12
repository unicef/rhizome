import _ from 'lodash'
import React, { Component, PropTypes } from 'react'
import format from 'utilities/format'

import Highcharts from 'highcharts'
window.Highcharts = Highcharts
import More from 'highcharts-more'
import Exporting from 'highcharts/modules/exporting'
import Map from 'highcharts/modules/map'
import themes from 'components/highchart/themes'
import palettes from 'utilities/palettes'

More(Highcharts)
Exporting(Highcharts)
Map(Highcharts)

class HighChart extends Component {

  constructor (props) {
    super(props)
    Highcharts.setOptions(themes.standard)
  }

  static propTypes = {
    config: React.PropTypes.object.isRequired,
    map: React.PropTypes.bool,
    isPureConfig: React.PropTypes.bool,
    neverReflow: React.PropTypes.bool
  }

  static defaultProps = {
    isPureConfig: true
  }

  componentDidMount = function () {
    this.renderChart()
  }

  componentWillUnmount = function () {
    this.chart.destroy()
  }

  shouldComponentUpdate = function (nextProps)  {
    const toggledEditMode = nextProps.editMode !== this.props.editMode
    if ((this.props.neverReflow || this.props.isPureConfig) && !toggledEditMode)  {
      return true
    }
    this.renderChart()
    return false
  }

  setConfig = function () {
    this.config = {}
  }

  getChart = function () {
    if (!this.chart) {
      throw new Error('getChart() should not be called before the component is mounted')
    }
    return this.chart
  }

  renderChart = function () {
    const type = this.props.type
    this.setConfig()
    const chartConfig = this.config.chart
    //refactor next line out to more centralized static param, especially if more map types added
    const chartType = type === 'MapChart' || type === 'BubbleMap' ? 'Map' : 'Chart'

    this.chart = new Highcharts[chartType]({
      ...this.config,
      chart: {
        ...chartConfig,
        className: 'overflow-hidden',
        renderTo: this.refs.chart.getDOMNode()
      }
    })
    global.requestAnimationFrame && requestAnimationFrame(()=>{
      this.chart && this.chart.options && this.chart.reflow()
    })
  }

  render = function () {
    return <div ref='chart' {...this.props} />
  }
}

export default HighChart

