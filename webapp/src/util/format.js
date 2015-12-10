import d3 from 'd3'
import moment from 'moment'

function general (value) {
  var mantissa = Math.abs(value) - Math.floor(Math.abs(value))
  return d3.format(mantissa > 0 ? '.4f' : 'n')(value)
}

function timeAxis (value) {
  var m = moment(value)

  return m.format(m.month() === 0
    ? 'YYYY'
    : 'MMM'
  )
}

export default {
  general: general,
  timeAxis: timeAxis
}
