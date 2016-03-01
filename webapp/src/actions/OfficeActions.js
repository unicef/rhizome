import Reflux from 'reflux'
import OfficeAPI from 'data/requests/OfficeAPI'

const OfficeActions = Reflux.createActions({
  'fetchOffices': { children: ['completed', 'failed'], asyncResult: true }
})

OfficeActions.fetchOffices.listenAndPromise(() => {
  return OfficeAPI.getOffices()
})

export default OfficeActions
