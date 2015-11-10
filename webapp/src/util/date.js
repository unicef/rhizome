'use strict'

/**
 * Split a string into tokens that can be passed to moment.duration.
 *
 * @param {String} value - A string of the format '<Number> <unit>' or simply
 *         '<Number>'
 *
 * @return an array containing one or two tokens, the first object in the array
 *     will be a Number, the second a String
 */
function parseDuration (value) {
  var toks = value.split(/\s+/)

  if (toks.length === 1) {
    return toks
  }

  if (toks.length !== 2) {
    throw new Error(value + ' cannot be parsed into a duration: too many spaces')
  }

  return [Number(toks[0]), toks[1]]
}

module.exports = {
  parseDuration: parseDuration
}
