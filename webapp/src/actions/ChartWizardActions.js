import Reflux from 'reflux'

let ChartWizardActions = Reflux.createActions([
  'initialize',
  'addIndicator',
  'removeIndicator',
  'changeChart',
  'previewChart'
])

export default ChartWizardActions
