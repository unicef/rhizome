'use strict'

var _ = require('lodash')

/**
 * Map properties on an object to new properties.
 *
 * @param {Object} - d The object whose properties will be mapped to a new object
 * @param {Object} - mapping of property names to functions that calculate the
 *   value for the newly mapped property.
 *
 * @return {Object} A new object with properties carried over from `d` and
 *  renamed according to `mapping` or transferred directly
 */
module.exports = function (d, mapping) {
    var o = {}

    // Map properties from old names to new
    _.each(mapping, function (v, k) {
        if (d.hasOwnProperty(k)) {
            o[v] = d[k]
        }
    })

    // Carry over any other properties directly
    for (var i = arguments.length - 1 i > 2 --i) {
        var k = arguments[i]

        if (d.hasOwnProperty(k)) {
            o[k] = d[k]
        }
    }

    return o
}
