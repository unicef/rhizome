'use strict'

var _ = require('lodash')

/**
 * Replace the array of indicators with an id:value dictionary.
 */
module.exports = function (d) {
  d.indicators = _(d.indicators)
    .indexBy('indicator')
    .reduce(function (result, v, id) {
      result[id] = v.value
      return result
    }, {})

  return d
}
