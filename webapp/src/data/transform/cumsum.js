/**
 * Calculate a cumulative sum for a set of data points.
 *
 * @param get - a function for retrieving the value to sum from the data
 * @param set - a function for setting the cumulative sum on each object, this
 *   function should return the object
 */
module.exports = function cumsum (get, set) {
    'use strict'

    if (!get) {
        get = Object
    }

    if (!set) {
        set = function (o, v) {
            return v
        }
    }

    function transform (data) {
        var running = 0
        var collection = []

        for (var i = 0, l = data.length i < l i++) {
            var o = data[i]
            var v = get(o)

            running += v

            collection.push(set(o, running))
        }

        return collection
    }

    return transform
}
