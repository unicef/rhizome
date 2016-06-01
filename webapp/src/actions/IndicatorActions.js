import Reflux from 'reflux'
import api from 'utilities/api'

const IndicatorActions = Reflux.createActions({
  'fetchIndicators': { children: ['completed', 'failed'] },
  'fetchIndicatorTags': { children: ['completed', 'failed'] },
  'fetchIndicatorsToTags': { children: ['completed', 'failed'] }
})

IndicatorActions.fetchIndicators.listenAndPromise(() => {
  return api.indicators(null, null, { 'cache-control': 'no-cache' })
})

IndicatorActions.fetchIndicatorTags.listenAndPromise(() => {
  return api.get_indicator_tag(null, null, { 'cache-control': 'no-cache' })
})

IndicatorActions.fetchIndicatorsToTags.listenAndPromise(() => api.indicator_to_tag())

export default IndicatorActions
