import _ from 'lodash'

function defined (value, accessor = _.identity) {
  var v = accessor(value)
  return !!v && Math.abs(v) !== Infinity
}

function rename (obj, mapping) {
  var o = {}

  for (var k in obj) {
    o[mapping[k] || k] = obj[k]
  }

  return o
}

function unpivot (data) {
  return _(data.objects)
    .map(function (d) {
      let {indicators, ...props} = d
      return indicators.map(indicator => {
        return Object.assign({}, {
          indicator: indicator.indicator,
          value: indicator.value
        }, props)
      }).reverse()
    })
    .flatten()
    .value()
}

export default {
  defined: defined,
  rename: rename,
  unpivot: unpivot
}
