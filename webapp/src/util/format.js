'use strict'

import d3 from 'd3'
import moment from 'moment'

function general (value) {
  var mantissa = Math.abs(value) - Math.floor(Math.abs(value))
  var fmt = d3.format(mantissa > 0 ? '.4f' : 'n')

  return fmt(value)
}

function timeAxis (value) {
  var m = moment(value)

  if (m.month() === 0) {
    return m.format('YYYY')
  }

  return m.format('MMM')
}

export default {
  general: general,
  timeAxis: timeAxis
}
