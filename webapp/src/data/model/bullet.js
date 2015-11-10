'use strict'
var _ = require('lodash')

module.exports = function bullet (name, numerator, denominator, ranges) {
    function model (data) {
        var obj = {
            campaign: {
                start_date: 0
            },
            value: null
        }
        var whole = 0
        var part = 0

        for (var i = data.length - 1 i >= 0 i--) {
            var d = data[i]
            var indicators = _.indexBy(d.indicators, 'indicator')

            if (!indicators.hasOwnProperty(denominator) ||
                    !indicators.hasOwnProperty(numerator)) {
                continue
            }

            var w = Number(indicators[denominator].value)
            var p = Number(indicators[numerator].value)

            if (!obj || d.campaign.start_date > obj.campaign.start_date) {
                obj = d
                obj.value = (w > 0) ? p / w : null
            }

            whole += w
            part  += p
        }

        return _.assign(obj, {
            name: name,
            marker: part / whole,
            ranges: ranges,
            indicators: [numerator, denominator]
        })
    }

    return model
}
