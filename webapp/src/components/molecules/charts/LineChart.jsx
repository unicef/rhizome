import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import format from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import LineChartRenderer from 'components/molecules/charts/renderers/line-chart'
import aspects from 'components/molecules/charts/utils/aspects'

class LineChart extends Component {

  static propTypes = {
    data: PropTypes.array,
    domain: PropTypes.array,
    range: PropTypes.array,
    annotated: PropTypes.bool,
    hasDots: PropTypes.bool,
    scale: PropTypes.func,
    xLabel: PropTypes.string,
    yLabel: PropTypes.string,
    xFormat: PropTypes.func,
    yFormat: PropTypes.func,
    colors: PropTypes.array,
    aspect: PropTypes.number,
    height: PropTypes.number,
    width: PropTypes.number,
    margin: PropTypes.shape({
       top: PropTypes.number,
       right: PropTypes.number,
       bottom: PropTypes.number,
       left: PropTypes.number,
    }),
    seriesName: PropTypes.func,
    values: PropTypes.func,
    x: PropTypes.func,
    y: PropTypes.func,
  }

  static defaultProps = {
    data: [],
    domain: null,
    range: null,
    annotated: false,
    hasDots: false,
    scale: d3.scale.linear,
    xLabel: null,
    yLabel: null,
    xFormat: format.timeAxis,
    yFormat: d3.format(',d'),
    colors: palettes.blue,
    aspect: aspects[1].lineChart,
    height: 0,
    width: 0,
    margin: { top: 12, right: 0, bottom: 20, left: 0 },
    seriesName: d => d.name,
    values: d => d.values,
    x: d => d.campaign.start_date,
    y: d => d.value
  }

  constructor(props) {
    console.info('------ LineChart.constructor')
    super(props)
    this.params = props
  }

  componentDidMount () {
    console.info('------ LineChart.componentDidMount')
    this.container = React.findDOMNode(this)
    const chart = this.getParams()
    this.chart = new LineChartRenderer(chart.data, chart, this.container)
    this.chart.render()
  }

  componentDidUpdate () {
    console.info('------ LineChart.componentDidUpdate')
    this.params = _.defaults({}, this.props, this.params)
    const chart = this.getParams()
    this.chart.update(chart.data, chart, this.container)
  }

  getParams () {
    console.info('------ LineChart.getParams')
    const aspect = this.params.aspect || 1
    this.params.width = this.props.width || this.container.clientWidth
    this.params.height = this.props.height || this.params.width / aspect
    this.params.colors = this.props.colors || this.props.color
    return this.params
  }

  render () {
    console.info('------ LineChart.render')
    return (
      <svg className='line'>
      </svg>
    )
  }
}

export default LineChart

