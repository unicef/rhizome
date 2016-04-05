import _ from 'lodash'
import d3 from 'd3'
import React, { PropTypes } from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import aspects from 'components/molecules/charts/utils/aspects'

class BarChart extends HighChart {
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
    height: 0,
    width: 0,
    margin: { top: 20, right: 30, bottom: 30, left: 20 },
    seriesName: d => d.name,
    values: d => d.values,
    x: d => d.campaign.start_date,
    y: d => d.value
  }

  setData () { console.info('------ BarChart.setData')
    const props = this.props
    const selected_locations_index = _.indexBy(props.selected_locations, 'id')
    const selected_indicators_index = _.indexBy(props.selected_indicators, 'id')

  }

  setOptions () { console.info('------ BarChart.setOptions')
    const options = this.options
    const props = this.props
  }
}

BarChart.propTypes = {
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

export default BarChart

