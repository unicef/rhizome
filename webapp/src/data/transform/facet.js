var _ = require('lodash')

module.exports = function facet (get) {
    'use strict'

    if (typeof get !== 'function') {
        get = function (o) {
            return o[get]
        }
    }

    function transform (data) {
        return _.values(_.groupBy(data, get))
    }

    return transform
}
