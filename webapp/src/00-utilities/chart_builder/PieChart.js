import _ from 'lodash'
import aspects from '00-utilities/chart_builder/aspects'

const processPieChart = (dataPromise, indicators, layout) => {
  const idx = _.indexBy(indicators, 'id')

  return dataPromise.then(function (data) {
    if (!data || data.length === 0) {
      return { options: null, data: null }
    }
    const total = _(data).map(function (n) { return n.value }).sum()
    const chartOptions = {
      aspect: aspects[layout].pieChart,
      domain: _.constant([0, total]),
      name: d => _.get(idx, '[' + d.indicator + '].name', ''),
      margin: {
        top: 10,
        right: 30,
        bottom: 10,
        left: 10
      }
    }
    return { options: chartOptions, data: data }
  })
}

export default processPieChart
