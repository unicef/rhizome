var _ = require('lodash')

module.exports = function treeify (data, idKey) {
    'use strict'
    var index = _.indexBy(data, idKey)
    var roots = []

    for (var i = data.length - 1; i >= 0; i--) {
        var d = data[i]

        if (d.parent && index[d.parent]) {
            var p = index[d.parent]

            if (!p.children) {
                p.children = []
            }

            p.children.push(d)
        } else {
            roots.push(d)
        }
    }

    return roots
}
