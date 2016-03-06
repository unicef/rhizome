const chartOptionsHelpers = {
  generateMarginForAxisLabel: (options) => {
    if (options.xLabel || options.yLabel) {
      let marginLeft = options.yLabel ? 15 : options.margin.left || 0
      let marginBottom = options.xLabel ? 30 : options.margin.bottom || 0
      let marginTop = options.margin.top || 0
      let marginRight = options.margin.right || 0
      options['margin'] = {top: marginTop, right: marginRight, bottom: marginBottom, left: marginLeft}
    }
    return options
  }
}

export default chartOptionsHelpers
