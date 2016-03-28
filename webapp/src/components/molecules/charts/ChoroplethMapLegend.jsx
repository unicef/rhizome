import d3 from 'd3'
import React, { PropTypes } from 'react'

import Chart from 'components/molecules/charts/Chart'
import format from 'components/molecules/charts/utils/format'
import palettes from 'components/molecules/charts/utils/palettes'
import aspects from 'components/molecules/charts/utils/aspects'

class ChoroplethMapLegend extends Chart {
  static defaultProps = {
    data: [],
    data_format: 'pct',
    colors: palettes.orange,
    onClick: null,
    yFormat: d => d3.format(Math.abs(d) < 1 ? '.4f' : 'n')(d),
    name: d => d.properties.name,
    maxBubbleValue: 5000,
    maxBubbleRadius: 25,
    bubbleLegendRatio: [0.1, 0.5, 1]
  }


  setOptions () {
    console.info('------ ChoroplethMapLegend.setOptions')
    const options = this.options
    const props = this.props
    const aspect = options.aspect || 1
    options.type = 'ChoroplethMapLegend'
    options.width = props.width || this.container.clientWidth
    options.height = props.height || options.width / aspect
    options.colors = props.colors || props.color

    return this.options
  }
}

ChoroplethMapLegend.propTypes = {
  data: PropTypes.array,
  data_format: PropTypes.string,
  colors: PropTypes.array,
  onClick: PropTypes.func,
  yFormat: PropTypes.func,
  name: PropTypes.func,
  maxBubbleValue: PropTypes.number,
  maxBubbleRadius: PropTypes.number,
  bubbleLegendRatio: PropTypes.arrayOf(PropTypes.number),
  colors: PropTypes.array,
  aspect: PropTypes.number,
  height: PropTypes.number,
  width: PropTypes.number,
  margin: PropTypes.shape({
     top: PropTypes.number,
     right: PropTypes.number,
     bottom: PropTypes.number,
     left: PropTypes.number,
  })
}

export default ChoroplethMapLegend

