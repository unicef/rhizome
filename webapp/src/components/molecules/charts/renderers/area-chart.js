import _ from 'lodash'
import d3 from 'd3'

import format from 'components/molecules/charts/utils/format'
import hoverLine from 'components/molecules/charts/renderers/common/hover-line'
import label from 'components/molecules/charts/renderers/common/label'

class AreaChartRenderer {
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

export default AreaChartRenderer
