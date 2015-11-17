import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import React from 'react'

var series = function (values, name) {
  return {
    name: name,
    values: _.sortBy(values, _.result('campaign.start_date.getTime'))
  }
}

var percentage = function (dataset) {
  var total = _(dataset).pluck('value').sum()

  _.forEach(dataset, function (d) {
    d.value /= total
  })

  return dataset
}

let dateFormat = d3.time.format("%B %Y")

function generateMissedChildrenChartData (original) {
  var stack = d3.layout.stack()
    .order('default')
    .offset('zero')
    .values(_.property('values'))
    .x(_.property('campaign.start_date'))
    .y(_.property('value'))

  var missed
  try {
    missed = _(original)
      .forEach(d => {
        if (_.isEqual(d.indicator.id, 164)) { d.indicator.short_name = 'Absent' }
        if (_.isEqual(d.indicator.id, 165)) { d.indicator.short_name = 'Other' }
      })
      .groupBy('indicator.short_name')
      .map(series)
      .thru(stack)
      .value()
  } catch (err) {
    console.error(err)
    console.log(`Data error in ${original}`)
    missed = []
  }

  return missed
}

function preparePolioCasesData (original) {
  var campaign = original.campaign
  var year = ''
  var totalCases = null
  var newCases = null

  if (campaign) {
    var m = moment(campaign.start_date, 'YYYY-MM-DD')
    year = m.format('YYYY')

    // Sum all of the reported Polio cases for the year
    totalCases = _(original.data)
      .filter(function (d) { return d.campaign.start_date.getFullYear() === year })
      .pluck('value')
      .sum()

    // Find the number of reported cases for this campaign
    newCases = _.get(
      _.find(
        original.data,
        function (d) { return d.campaign.start_date.getTime() === m.valueOf() }
      ),
      'value'
    )
  }

  // Set the title based on whether there is data
  var title = <h4 className='chart-title'>
        <span style={{
          'color': '#F18448'
        }}>{totalCases} Polio cases this year</span>
  </h4>

  var newCaseLabel = ''

  if (_.isFinite(newCases) && newCases > 0) {
    var plural = newCases !== 1 ? 's' : ''
    newCaseLabel = (
      <div id='new-polio-cases'style={{position: 'absolute', color: '#D84E43'}}>
        {newCases} new case{plural}
      </div>
    )
  }

  return {
    title: title,
    newCaseLabel: newCaseLabel,
    data: original.data,
    date: dateFormat(new Date(original.campaign.start_date))
  }
}

function prepareMissedChildrenData (original) {
  var data = original.data
  var campaign = original.campaign
  var location = original.location

  var upper = moment(campaign.start_date, 'YYYY-MM-DD')
  var lower = upper.clone().startOf('month').subtract(1, 'year')

  var missed = generateMissedChildrenChartData(data.missedChildren)

  var missedScale = [lower.valueOf(), upper.valueOf()]

  var missedChildrenMap = data.missedChildrenByProvince

  return {
    missedChildrenMap: missedChildrenMap,
    missed: missed,
    missedScale: missedScale,
    location: location,
    date: dateFormat(new Date(original.campaign.start_date))
  }
}

function prepareUnderImmunizedData (original) {
  var stack = d3.layout.stack()
    .offset('zero')
    .values(function (d) { return d.values })
    .x(function (d) { return d.campaign.start_date })
    .y(function (d) { return d.value })

  var data = _(original.data)
    .each(function (d) {
      // Add a property to each datapoint indicating the fiscal quarter
      d.quarter = moment(d.campaign.start_date).format('[Q]Q YYYY')
    })
    .groupBy(function (d) {
      return d.indicator.id + '-' + d.quarter
    })
    .map(function (datapoints) {
      // Calculate the total number of children with X doses of OPV for
      // each quarter
      return _.assign({}, datapoints[0], {
        'value': _(datapoints).pluck('value').sum()
      })
    })
    .groupBy('quarter')
    .map(percentage)
    .flatten()
    .reject(function (d) {
      // Exclude 4+ doses, because that is implied as 1 - <0 doses> - <1–3 doses>
      return d.indicator.id === 433
    })
    .groupBy('indicator.short_name')
    .map(function (values, name) {
      return {
        name: name,
        values: values
      }
    })
    .sortBy('name')
    .value()

  var start = moment(original.campaign.start_date)
  var lower = start.clone().startOf('quarter').subtract(3, 'years')
  var upper = start.clone().endOf('quarter')

  var immunityScale = _.map(d3.time.scale()
      .domain([lower.valueOf(), upper.valueOf()])
      .ticks(d3.time.month, 3),
    _.method('getTime')
  )

  var color = _.flow(
    _.property('name'),
    d3.scale.ordinal()
      .domain(_(data).pluck('name').sortBy().value())
      .range(['#D95449', '#B6D0D4'])
  )

  return {
    data: stack(data),
    immunityScale: immunityScale,
    color: color,
    date: dateFormat(new Date(original.campaign.start_date))
  }
}

export default {
  preparePolioCasesData: preparePolioCasesData,
  prepareMissedChildrenData: prepareMissedChildrenData,
  prepareUnderImmunizedData: prepareUnderImmunizedData
}
