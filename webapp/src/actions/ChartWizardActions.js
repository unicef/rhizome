import Reflux from 'reflux'

let ChartWizardActions = Reflux.createActions([
  'initialize',
  'editTitle',
  'addLocation',
  'addIndicator',
  'removeIndicator',
  'addCampaign',
  'changeChart',
  'changeGroupRadio',
  'changeTimeRadio',
  'changeYFormatRadio',
  'saveChart'
])

export default ChartWizardActions
