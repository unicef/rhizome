import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes, Component } from 'react'

import ColumnChartRenderer from 'components/molecules/charts/renderers/column-chart'

const DEFAULTS = {
}

class ColumnChart extends Component {
  constructor(props) {
    super(props)
    this.options = _.defaults({}, props.options, DEFAULTS)
  }

  componentDidMount () {
    this.container = React.findDOMNode(this)
    this.chart = new ColumnChartRenderer(this.props.data, this.options, this.container)
    this.chart.render()
  }

  componentDidUpdate () {
    this.chart.update(this.props.data, this.options, this.container)
  }

  render () {
    return (

    )
  }
}

export default ColumnChart

