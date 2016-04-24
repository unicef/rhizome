import api from 'data/api'

export default {
  putComputedDatapoint (options) {
    let fetch = api.endPoint('/computed_datapoint/' + options.computed_id, 'PATCH', 1)
    return new Promise(function (fulfill, reject) {
      fetch({value: options.value}, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      }, reject)
    })
  },
  postComputedDatapoint (options) {
    console.log('options: ', options)
    delete options['computed_id']
    let fetch = api.endPoint('/computed_datapoint/', 'POST', 1)
    return new Promise(function (fulfill, reject) {
      fetch(options, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      }, reject)
    })
  },
  deleteComputedDataPoint (id) {
    let fetch = api.endPoint('/computed_datapoint/' + id, 'delete', 1)
    return new Promise(function (fulfill, reject) {
      fetch(null, null, {'cache-control': 'no-cache'}).then(function (computed_datapoint) {
        fulfill(computed_datapoint)
      })
    })
  }
}
