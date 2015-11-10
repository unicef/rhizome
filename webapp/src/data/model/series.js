module.exports = function (name) {
    'use strict'

    function model (data) {
        var series = {
            points: data
        }

        if (name) {
            if (typeof name === 'function') {
                series.name = name(data)
            } else {
                series.name = name
            }
        }

        return series
    }

    return model
}
