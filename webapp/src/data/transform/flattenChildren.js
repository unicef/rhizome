var _ = require('lodash')

/**
 * Assemble a flat array with all an object's nested children (deep)
 */
function flattenChildren (root, childrenKey, arr, filterCondition, maxDepth) {
    'use strict'

    arr = arr || []

    if (!_.isNumber(maxDepth)) {
        maxDepth = Infinity
    }

    if (maxDepth < 1) {
        return arr
    }

    if (root[childrenKey] && _.isArray(root[childrenKey])) {
        _.forEach(root[childrenKey], function (child) {
            if (!filterCondition || filterCondition(child)) {
                arr.push(child)
            }
            flattenChildren(child, childrenKey, arr, filterCondition, maxDepth - 1)
        })
    }

    return arr
}

module.exports = flattenChildren
