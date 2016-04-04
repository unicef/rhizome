import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes } from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import aspects from 'components/molecules/charts/utils/aspects'

class LineChart extends HighChart {
  static defaultProps = {
    data: [],
    domain: null,
    groupBy: 'indicator',
    range: null,
    annotated: true,
    hasDots: true,
    scale: d3.scale.linear,
    xLabel: null,
    yLabel: null,
    xFormat: format.timeAxis,
    yFormat: d3.format(',d'),
    colors: palettes.dark,
    aspect: aspects[1].lineChart,
    height: 0,
    width: 0,
    margin: { top: 20, right: 30, bottom: 30, left: 20 },
    seriesName: d => d.name,
    values: d => d.values,
    x: d => d.campaign.start_date,
    y: d => d.value
  }

  setData () { console.info('------ LineChart.setData')
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

  setOptions () { console.info('------ LineChart.setOptions')
    const options = this.options
    const props = this.props
    const aspect = options.aspect || 1
    this.options.width = props.width || this.container.clientWidth
    this.options.height = props.height || this.options.width / aspect
    this.options.colors = props.colors || props.color
    if (options.groupBy === 'indicator') {
      if (this.props.selected_indicators[0].data_format === 'pct') {
        this.options.yFormat = d3.format(',.1%')
      }
    } else if (options.groupBy === 'location') {
      // To do
    }
    if (props.xLabel || props.yLabel) {
      let marginLeft = props.yLabel ? 15 : props.margin.left || 0
      let marginBottom = props.xLabel ? 30 : props.margin.bottom || 0
      let marginTop = props.margin.top || 0
      let marginRight = props.margin.right || 0
      this.options.margin = {top: marginTop, right: marginRight, bottom: marginBottom, left: marginLeft}
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

