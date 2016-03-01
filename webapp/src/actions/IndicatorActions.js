import Reflux from 'reflux'
import IndicatorAPI from 'data/requests/IndicatorAPI'

const IndicatorActions = Reflux.createActions({
  'fetchIndicators': { children: ['completed', 'failed'], asyncResult: true }
})

IndicatorActions.fetchIndicators.listenAndPromise(() => {
  return IndicatorAPI.getIndicators()
})

export default IndicatorActions
