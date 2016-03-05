import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import React from 'react'

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
      .filter(function (d) { return d.campaign.start_date.getFullYear().toString() === year })
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
  var title = <h4>
        <span style={{
          'color': '#F18448'
        }}>{totalCases} Polio cases this year</span>
  </h4>

  newCases = (_.isFinite(newCases) && newCases > 0) ? newCases : 0

  var plural = newCases !== 1 ? 's' : ''
  var newCaseLabel = (
    <h4>
        <span style={{
          'color': '#F15046'
        }}>{newCases} new case{plural}</span>
    </h4>
  )

  return {
    title: title,
    newCaseLabel: newCaseLabel,
    data: original.data,
    date: moment(original.campaign.start_date).format('MMMM YYYY')
  }
}

function prepareMissedChildrenData (original) {
  var data = original.data
  var campaign = original.campaign
  var location = original.location

  var upper = moment(campaign.start_date, 'YYYY-MM-DD')
  var lower = upper.clone().startOf('month').subtract(1, 'year')

  var missedScale = [lower.valueOf(), upper.valueOf()]

  var missedChildrenMap = data.missedChildrenByProvince

  var missed = _(data.missedChildren)
    .forEach(d => {
      if (_.isEqual(d.indicator.id, 164)) { d.indicator.short_name = 'Absent' }
      if (_.isEqual(d.indicator.id, 165)) { d.indicator.short_name = 'Other' }
    })

  return {
    missedChildrenMap: missedChildrenMap,
    missed: missed,
    missedScale: missedScale,
    location: location,
    date: moment(original.campaign.start_date).format('MMMM YYYY')
  }
}

function prepareUnderImmunizedData (original) {
  var start = moment(original.campaign.start_date)
  var lower = start.clone().startOf('quarter').subtract(3, 'years')
  var upper = start.clone().endOf('quarter')

  var immunityScale = _.map(d3.time.scale()
      .domain([lower.valueOf(), upper.valueOf()])
      .ticks(d3.time.month, 3),
    _.method('getTime')
  )

  var color = ['#D95449', '#B6D0D4']

  return {
    data: original.data,
    immunityScale: immunityScale,
    color: color,
    date: moment(original.campaign.start_date).format('MMMM YYYY')
  }
}

export default {
  preparePolioCasesData: preparePolioCasesData,
  prepareMissedChildrenData: prepareMissedChildrenData,
  prepareUnderImmunizedData: prepareUnderImmunizedData
}
