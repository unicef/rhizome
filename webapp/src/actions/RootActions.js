import Reflux from 'reflux'
import api from 'data/api'

const RootActions = Reflux.createActions({
  'fetchAllMeta': { children: ['completed', 'failed'] }
})

// API CALLS
// ---------------------------------------------------------------------------
RootActions.fetchAllMeta.listenAndPromise(() => api.get_all_meta(null, null, {'cache-control': 'no-cache'}))

export default RootActions
