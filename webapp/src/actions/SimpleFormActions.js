import Reflux from 'reflux'

export default Reflux.createActions([
  'currentIndicatorPromise',
  'initialize',
  'baseFormSave',
  'addTagToIndicator',
  'addIndicatorToTag',
  'removeIndicatorFromTag',
  'removeTagFromIndicator',
  'addCalculationToIndicator',
  'removeCalculationFromIndicator',
  'getTagTree',
  'initIndicatorToTag',
  'initTagToIndicator',
  'initIndicatorToCalc',
  'refreshTags',
  'refreshCalculation',
  'refreshIndicators',
  'getIndicators'
])
