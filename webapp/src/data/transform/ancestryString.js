'use strict'

import _ from 'lodash'

function setAncestryStringRecursive (data) {
  _.each(_.get(data, 'children', []), function (child) {
    child.ancestryString = _.get(data, 'ancestryString', '') + data.title + ' > '

    setAncestryStringRecursive(child)
  })

  return data
}

export default setAncestryStringRecursive
