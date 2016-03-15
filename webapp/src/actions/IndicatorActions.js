import Reflux from 'reflux'
import api from 'data/api'

const IndicatorActions = Reflux.createActions({
  'fetchIndicators': { children: ['completed', 'failed'], asyncResult: true },
  'fetchIndicatorTags': { children: ['completed', 'failed'], asyncResult: true },
  'selectIndicator': 'selectIndicator',
  'deselectIndicator': 'deselectIndicator',
  'reorderIndicator': 'reorderIndicator',
  'clearSelectedIndicators': 'clearSelectedIndicators'
})

IndicatorActions.fetchIndicators.listenAndPromise(() => {
  return api.indicators(null, null, { 'cache-control': 'no-cache' })
})

IndicatorActions.fetchIndicatorTags.listenAndPromise(() => {
  return api.get_indicator_tag(null, null, { 'cache-control': 'no-cache' })
})

export default IndicatorActions
