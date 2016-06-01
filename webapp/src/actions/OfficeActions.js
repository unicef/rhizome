import Reflux from 'reflux'
import api from 'utilities/api'

const OfficeActions = Reflux.createActions({
  'fetchOffices': { children: ['completed', 'failed'], asyncResult: true }
})

OfficeActions.fetchOffices.listenAndPromise(() => {
  return api.office(null, null, {'cache-control': 'max-age=604800, public'})
})

export default OfficeActions
