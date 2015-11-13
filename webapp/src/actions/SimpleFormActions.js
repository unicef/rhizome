'use strict'

import Reflux from 'reflux'

export default Reflux.createActions([
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
