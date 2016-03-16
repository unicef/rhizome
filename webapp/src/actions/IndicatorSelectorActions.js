import Reflux from 'reflux'

const IndicatorSelectorActions = Reflux.createActions({
  'selectIndicator': 'selectIndicator',
  'deselectIndicator': 'deselectIndicator',
  'reorderIndicator': 'reorderIndicator',
  'setSelectedIndicators': 'setSelectedIndicators',
  'clearSelectedIndicators': 'clearSelectedIndicators'
})

export default IndicatorSelectorActions
