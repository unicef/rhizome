'use strict'

import Reflux from 'reflux'

module.exports = Reflux.createActions([
  'currentIndicatorPromise',
  'initialize',
  'baseFormSave',
  'addTagToIndicator',
  'removeTagFromIndicator',
  'addCalculationToIndicator',
  'removeCalculationFromIndicator',
  'getTagTree',
  'initIndicatorToTag',
  'initIndicatorToCalc',
  'refreshTags',
  'refreshCalculation'
])
