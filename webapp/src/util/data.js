'use strict'

var _ = require('lodash')
var path = require('vue/src/parsers/path')

/**
 * Return an accessor name for `prop`.
 *
 * Returns an accessor function that takes an object (d) as an argument and
 * looks up the value at the path specified by `prop`.
 *
 * @example
 * // Returns the value at d.foo
 * accessor('foo')(d)
 *
 * // Returns the value at d.foo.bar[0]
 * accessor('foo.bar[0]')(d)
 *
 * @param {String} prop A path to the property to access on objects
 */
function accessor (prop) {
  return function (d) {
    var v = path.get(d, prop)

    if (_.isDate(v)) {
      return v.getTime()
    }

    return v
  }
}

function defined (value, accessor) {
  if (arguments.length < 2) {
    accessor = _.identity
  }

  var v = accessor(value)

  return v !== null &&
    typeof v !== 'undefined' &&
    Math.abs(v) !== Infinity &&
    !isNaN(v)
}

function max (data, accessor) {
  var m = -Infinity

  accessor = accessor || Number

  if (data instanceof Array) {
    for (var i = data.length - 1; i >= 0; i--) {
      m = Math.max(m, max(data[i], accessor))
    }
  } else {
    var v = accessor(data)

    if (defined(v)) {
      m = Math.max(m, v)
    }
  }

  return m
}

function min (data, accessor) {
  var m = Infinity

  accessor = accessor || Number

  if (data instanceof Array) {
    for (var i = data.length - 1; i >= 0; i--) {
      m = Math.min(m, min(data[i], accessor))
    }
  } else {
    var v = accessor(data)

    if (defined(v)) {
      m = Math.min(m, v)
    }
  }

  return m
}

function parseBool (value) {
  if (value instanceof String) {
    return value === 'true'
  }

  return Boolean(value)
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
      var datapoints = []
      var indicators = d.indicators
      var props = _.omit(d, 'indicators')

      for (var i = indicators.length - 1; i >= 0; i--) {
        var datum = indicators[i]

        datapoints.push(_.assign({
          indicator: datum.indicator,
          value: datum.value
        }, props))
      }

      return datapoints
    })
    .flatten()
    .value()
}

module.exports = {
  accessor: accessor,
  defined: defined,
  max: max,
  min: min,
  parseBool: parseBool,
  rename: rename,
  unpivot: unpivot
}
