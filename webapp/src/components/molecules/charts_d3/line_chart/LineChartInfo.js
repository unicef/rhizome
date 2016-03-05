import _ from 'lodash'
import moment from 'moment'
import aspects from 'components/molecules/charts_d3/utils/aspects'
import chartOptionsHelpers from 'components/molecules/charts_d3/utils/chartOptionsHelpers'

const processLineChart = (dataPromise, lower, upper, groups, chartDef, layout) => {
  let groupBy = chartDef.groupBy

  return dataPromise.then(data => {
    if (!data || data.length === 0) {
      return { options: null, data: null }
    }

    if (!lower) { // set the lower bound from the lowest datapoint value
      const sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'))
      lower = moment(_.first(sortedDates).campaign.start_date)
    }

    const options = {
      domain: _.constant([lower.toDate(), upper.toDate()]),
      aspect: aspects[layout].lineChart,
      values: _.property('values'),
      x: _.property('campaign.start_date'),
      xFormat: (d) => { return moment(d).format('MMM YYYY') },
      y: _.property('value'),
      xLabel: chartDef.xLabel,
      yLabel: chartDef.yLabel
    }

    return {
      options: chartOptionsHelpers.generateMarginForAxisLabel(options),
      data: groupBySeries(data, groups, groupBy)
    }
  })
}

const groupBySeries = (data, groups, groupBy) => {
  return _(data)
    .groupBy(groupBy)
    .map((d, ind) => {
      return {
        name: groups[ind].name,
        values: _.sortBy(d, _.method('campaign.start_date.getTime'))
      }
    })
    .value()
}

export default processLineChart
