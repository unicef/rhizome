import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import aspects from 'components/molecules/charts_d3/utils/aspects'
import chartOptionsHelpers from 'components/molecules/charts_d3/utils/chartOptionsHelpers'

const processColumnChart = (dataPromise, lower, upper, groups, chartDef, layout) => {
  let groupBy = chartDef.groupBy
  return dataPromise.then(data => {
    if (!data || data.length === 0) {
      return { options: null, data: null }
    }
    if (!lower) { // set the lower bound from the lowest datapoint value
      const sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'))
      lower = moment(_.first(sortedDates).campaign.start_date)
    }
    const columnScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 1),
      _.method('getTime')
    )
    const chartData = columnData(data, groups, groupBy)

    let chartOptions = {
      aspect: aspects[layout].columnChart,
      values: _.property('values'),
      domain: _.constant(columnScale),
      x: d => {
        const start = d.campaign.start_date
        return moment(start).startOf('month').toDate().getTime()
      },
      xFormat: d => { return moment(d).format('MMM YYYY') },
      xLabel: chartDef.xLabel,
      yLabel: chartDef.yLabel,
      margin: {
        top: 20,
        right: 0,
        bottom: 0,
        left: 0
      }
    }

    chartOptions = chartOptionsHelpers.generateMarginForAxisLabel(chartOptions)
    return { options: chartOptions, data: chartData }
  })
}

const seriesObject = (d, ind, collection, groups) => {
  return {
    name: groups[ind].name,
    values: d
  }
}

const columnData = (data, groups, groupBy) => {
  const columnData = _(data)
    .groupBy(groupBy)
    .map(_.partialRight(seriesObject, groups))
    .value()
  const baseCampaigns = []
  columnData.forEach(series => {
    series.values.forEach(value => { // build the base campaign array that includes all campaigns present in any datapoint, used to fill in missing values so the stacked chart doesn't have gaps
      if (!_.find(baseCampaigns, campaign => { return campaign.id === value.campaign.id })) {
        baseCampaigns.push(value.campaign)
      }
    })
    series.values.forEach(val => { // replace all null values with 0, caused d3 rect rendering errors in the chart
      if (_.isNull(val.value)) {
        val.value = 0
      }
    })
  })
  const sortedBaseCampaigns = _.sortBy(baseCampaigns, _.method('campaign.start_date.getTime'))
  columnData.forEach(series => {
    sortedBaseCampaigns.forEach((baseCampaign, index) => {
      if (!_.find(series.values, value => { return value.campaign.id === baseCampaign.id })) {
        series.values.splice(index, 0, { campaign: baseCampaign, location: series.values[0].location, indicator: series.values[0].indicator, value: 0 })
      }
    })
    series.values = _.sortBy(series.values, _.method('campaign.start_date.getTime'))
  })
  const stack = d3.layout.stack()
    .order('default')
    .offset('zero')
    .values(d => { return d.values })
    .x(d => { return d.campaign.start_date })
    .y(d => { return d.value })

  return stack(columnData)
}

export default processColumnChart
