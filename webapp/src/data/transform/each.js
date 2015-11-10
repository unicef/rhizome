
module.exports = function each (fn) {
    'use strict'

    function transform (data) {
        data.forEach(fn)

        return data
    }

    return transform
}
