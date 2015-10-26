import Reflux from 'reflux'

let ChartWizardActions = Reflux.createActions([
  'initialize',
  'editTitle',
  'addLocation',
  'addIndicator',
  'removeIndicator',
  'changeChart',
  'previewChart',
  'saveChart'
])

export default ChartWizardActions
