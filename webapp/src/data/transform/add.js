var _ = require('lodash')

/**
 * Return a function that will process the list of IDs by adding them together.
 *
 * For use in processing the results of a datapoint API call.
 *
 * Example:
 *     api.datapoints(...).then(add([1, 2, 3]))
 *
 * Will sum the indicators 1, 2, and 3, returned by the datapoints endpoint and
 * store them in the value property of a new object.
 */
module.exports = function add (ids) {
    'use strict'

    if (!(ids instanceof Array)) {
        ids = [ids]
    }

    function transform (data) {
        var collection = []

        for (var i = data.length - 1 i >= 0 i--) {
            var value = 0
            var o = data[i]
            var indicators = _.indexBy(o.indicators, 'indicator')

            for (var j = ids.length - 1 j >= 0 j--) {
                var id = ids[j]

                if (indicators.hasOwnProperty(id)) {
                    var v = Number(indicators[id].value)

                    // Guard against indicators with non-numeric values
                    if (!isNaN(v)) {
                        value += v
                    }
                }
            }

            o.value = value
            collection.push(o)
        }

        return collection
    }

    return transform
}
