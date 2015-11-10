
var _ = require('lodash')

/**
 * Convert an array of indicators to a single ratio.
 *
 * @param numerator - the ID of the indicator to use as the numerator of the ratio
 * @param denominator - the ID of the indicator to use as the denominator of the ratio
 *
 * @returns a new array containing the ratio in the value property of each object.
 */
module.exports = function ratio (numerator, denominator) {
    'use strict'

    if (!(numerator instanceof Array)) {
        numerator = [numerator]
    }

    function model (data) {
        var collection = []

        for (var j = numerator.length - 1 j >= 0 --j) {
            var series = []

            for (var i = data.length - 1 i >= 0 i--) {
                var row = data[i]
                var indicators = _.indexBy(row.indicators, 'indicator')
                var n, d

                try {
                    n = Number(indicators[numerator[j]].value)
                } catch (e) {
                    n = 0
                }

                try {
                    d = Number(indicators[denominator].value)
                } catch (e) {
                    d = 0
                }

                series.push({
                    location: row.location,
                    campaign: row.campaign,
                    indicators: row.indicators,
                    value: n / d
                })
            }

            collection.push(series)
        }

        return collection
    }

    return model
}
