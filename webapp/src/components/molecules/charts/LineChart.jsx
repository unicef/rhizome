import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes } from 'react'

import Chart from 'components/molecules/charts/Chart'
import format from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import aspects from 'components/molecules/charts/utils/aspects'

class LineChart extends Chart {
  static defaultProps = {
    data: [],
    domain: null,
    groupBy: 'indicator',
    range: null,
    annotated: false,
    hasDots: false,
    scale: d3.scale.linear,
    xLabel: null,
    yLabel: null,
    xFormat: format.timeAxis,
    yFormat: d3.format(',d'),
    colors: palettes.dark,
    aspect: aspects[1].lineChart,
    height: 0,
    width: 0,
    margin: { top: 12, right: 0, bottom: 20, left: 0 },
    seriesName: d => d.name,
    values: d => d.values,
    x: d => d.campaign.start_date,
    y: d => d.value
  }

  setData () {
    const props = this.props
    const selected_locations_index = _.indexBy(props.selected_locations, 'id')
    const selected_indicators_index = _.indexBy(props.selected_indicators, 'id')
    const groups = props.groupBy === 'indicator' ? selected_indicators_index : selected_locations_index
    this.data = _(props.data).groupBy(props.groupBy)
      .map(datapoint => {
        const first_indicator = datapoint[0].indicator
        return {
          name: groups[first_indicator.id].name,
          values: _.sortBy(datapoint, _.method('campaign.start_date.getTime'))
        }
      })
      .value()
  }

  setOptions () {
    console.info('------ LineChart.setOptions')
    const options = this.options
    const props = this.props
    const aspect = options.aspect || 1
    options.width = props.width || this.container.clientWidth
    options.height = props.height || options.width / aspect
    options.colors = props.colors || props.color
    if (props.xLabel || props.yLabel) {
      let marginLeft = props.yLabel ? 15 : props.margin.left || 0
      let marginBottom = props.xLabel ? 30 : props.margin.bottom || 0
      let marginTop = props.margin.top || 0
      let marginRight = props.margin.right || 0
      options.margin = {top: marginTop, right: marginRight, bottom: marginBottom, left: marginLeft}
    }
  }
}

LineChart.propTypes = {
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

export default LineChart

