var _ = require('lodash')

/**
 * Apply fn to each element in an array.
 *
 * For use processing the results of a datapoints API call using the then()
 * method of a Promise.
 */
module.exports = function map (fn) {
    'use strict'

    function transform (data) {
        return _.map(data, fn)
    }

    return transform
}
