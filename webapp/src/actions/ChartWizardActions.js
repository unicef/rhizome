import Reflux from 'reflux'

let ChartWizardActions = Reflux.createActions([
  'initialize',
  'editTitle',
  'addLocation',
  'addIndicator',
  'removeIndicator',
  'changeChart',
  'changeGroupRadio',
  'previewChart',
  'saveChart'
])

export default ChartWizardActions
