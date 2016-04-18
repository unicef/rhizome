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
  'initTagToIndicator',
  'initIndicatorToCalc',
  'refreshTags',
  'refreshCalculation',
  'getIndicators'
])
