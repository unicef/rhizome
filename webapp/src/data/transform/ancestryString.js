'use strict'

var _ = require('lodash')

function setAncestryStringRecursive (data) {
  _.each(_.get(data, 'children', []), function (child) {
    child.ancestryString = _.get(data, 'ancestryString', '') + data.title + ' > '

    setAncestryStringRecursive(child)
  })

  return data
}

module.exports = setAncestryStringRecursive
