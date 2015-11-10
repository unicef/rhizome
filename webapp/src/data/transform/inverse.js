module.exports = function inverse () {
  'use strict'

  function transform (data) {
    data.value = 1 - data.value
  }

  return transform
}
