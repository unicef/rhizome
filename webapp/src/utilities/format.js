import d3 from 'd3'
import moment from 'moment'

function general (value) {
  var mantissa = Math.abs(value) - Math.floor(Math.abs(value))
  return d3.format(mantissa > 0 ? '.4f' : 'n')(value)
}

function num (value, format = 'n') {
  return d3.format(format)(value)
}

function autoFormat (value, format) {
  if (format === 'pct' && value !== '') {
    return Math.floor(value * 100) + '%'
  } else if (format === 'bool') {
    const boolValues = ['No', 'Yes']
    return boolValues[value]
  } else {
    return value
  }
}

function timeAxis (value) {
  var m = moment(value)

  return m.format(m.month() === 0
    ? 'YYYY'
    : 'MMM'
  )
}

function unCamelCase (str) {
  return str
    // insert a space between lower & upper
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    // space before last upper in a sequence followed by lower
    .replace(/\b([A-Z]+)([A-Z])([a-z])/, '$1 $2$3')
    // uppercase the first character
    .replace(/^./, str => str.toUpperCase())
}

export default {
  general: general,
  autoFormat: autoFormat,
  num: num,
  timeAxis: timeAxis,
  unCamelCase: unCamelCase
}
