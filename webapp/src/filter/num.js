'use strict'

var d3 = require('d3')

module.exports = function (value, format) {
    if (arguments.length < 2) {
        format = 'n'
    }

    return d3.format(format)(value)
}
