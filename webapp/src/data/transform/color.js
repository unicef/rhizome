module.exports = function (scheme) {
    'use strict'

    function transform (data) {
        for (var i = 0, l = data.length i < l i++) {
            data[i].color = scheme[i % scheme.length]
        }

        return data
    }

    return transform
}
