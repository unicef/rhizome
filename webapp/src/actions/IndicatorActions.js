import Reflux from 'reflux'
import api from 'data/api'

const IndicatorActions = Reflux.createActions({
  'fetchIndicators': { children: ['completed', 'failed'] },
  'fetchIndicatorTags': { children: ['completed', 'failed'] }
})

IndicatorActions.fetchIndicators.listenAndPromise(() => {
  return api.indicators(null, null, { 'cache-control': 'no-cache' })
})

IndicatorActions.fetchIndicatorTags.listenAndPromise(() => {
  return api.get_indicator_tag(null, null, { 'cache-control': 'no-cache' })
})

export default IndicatorActions
