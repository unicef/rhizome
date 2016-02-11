import Reflux from 'reflux'

let ChartWizardActions = Reflux.createActions([
  'initialize',
  'clear',
  'editTitle',
  'changeCountry',
  'addLocation',
  'removeLocation',
  'clearSelectedLocations',
  'addFirstIndicator',
  'addIndicator',
  'reorderIndicator',
  'clearSelectedIndicators',
  'removeIndicator',
  'addCampaign',
  'changeChart',
  'changeGroupRadio',
  'changeLocationLevelRadio',
  'changeTimeRadio',
  'changeYFormatRadio',
  'changeXFormatRadio',
  'changeYAxis',
  'changeZAxis',
  'changePalette',
  'setXYAxisLabel',
  'saveChart',
  'updateDateRangePicker'
])

export default ChartWizardActions
