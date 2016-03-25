const chartOptionsHelpers = {
  generateMarginForAxisLabel: (chart) => {
    if (chart.xLabel || chart.yLabel) {
      let marginLeft = chart.yLabel ? 15 : chart.margin.left || 0
      let marginBottom = chart.xLabel ? 30 : chart.margin.bottom || 0
      let marginTop = chart.margin.top || 0
      let marginRight = chart.margin.right || 0
      chart['margin'] = {top: marginTop, right: marginRight, bottom: marginBottom, left: marginLeft}
    }
    return chart
  }
}

export default chartOptionsHelpers
