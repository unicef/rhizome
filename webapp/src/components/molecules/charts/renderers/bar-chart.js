import _ from 'lodash'
import d3 from 'd3'

import Tooltip from 'components/molecules/Tooltip.jsx'

import ColumnChart from 'components/molecules/charts/renderers/column-chart'
import legend from 'components/molecules/charts/renderers/common/legend'
import axisLabel from 'components/molecules/charts/renderer/common/axis-label'

import browser from 'components/molecules/charts/utils/browser'
import color from 'components/molecules/charts/utils/color'
import palettes from 'components/molecules/charts/utils/palettes'

class BarChartRenderer {
  constructor (data, options, container) {
    this.setChartParams(data, options, container)
  }

  setChartParams (data, options, container) {
    this.container = container
    this.options = options
    this.data = data
  }

  update () {
    this.setChartParams(this.data, this.options, this.container)
    this.render()
  }

  render () {
    this.renderXAxis()
    this.renderYAxis()
  }

  // =========================================================================== //
  //                                   RENDER                                    //
  // =========================================================================== //

  // X AXIS
  // ---------------------------------------------------------------------------
  renderXAxis () {
  }

  // Y AXIS
  // ---------------------------------------------------------------------------
  renderYAxis () {
  }
}

export default BarChartRenderer
