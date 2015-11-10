'use strict'

var Reflux = require('reflux')

module.exports = Reflux.createActions([
  'currentIndicatorPromise',
  'initialize',
  'baseFormSave',
  'addTagToIndicator',
  'removeTagFromIndicator',
  'addCalculationToIndicator',
  'removeCalculationFromIndicator',
  'addIndicatorCalc',
  'getTagTree',
  'initIndicatorToTag',
  'initIndicatorToCalc',
  'refreshTags',
  'refreshCalculation'
])
