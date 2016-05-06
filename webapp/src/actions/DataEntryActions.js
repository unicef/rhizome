import Reflux from 'reflux'
import api from 'data/api'

const DataEntryActions = Reflux.createActions({
  'postDatapoint': { children: ['completed', 'failed'] },
  'patchDatapoint': { children: ['completed', 'failed'] },
  'deleteDatapoint': { children: ['completed', 'failed'] },
  'initData': 'initData',
  'setIndicatorsByTag': 'setIndicatorsByTag',
  'setCampaign': 'setCampaign',
  'setSource': 'setSource',
  'addLocation': 'addLocation',
  'removeLocation': 'removeLocation',
  'changeSelect': 'changeSelect',
  'getTableData': 'getTableData'
})

DataEntryActions.postDatapoint.listenAndPromise(options => {
  delete options['computed_id']
  let fetch = api.endPoint('/computed_datapoint/', 'POST', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

DataEntryActions.patchDatapoint.listenAndPromise(options => {
  let fetch = api.endPoint('/computed_datapoint/' + options.computed_id, 'PATCH', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

DataEntryActions.deleteDatapoint.listenAndPromise(id => {
  let fetch = api.endPoint('/computed_datapoint/' + id, 'DELETE', 1)
  return fetch(null, null, {'cache-control': 'no-cache'})
})

export default DataEntryActions
