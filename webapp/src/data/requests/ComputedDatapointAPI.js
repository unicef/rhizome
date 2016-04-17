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
    let fetch = api.endPoint('/computed_datapoint/', 'POST', 1)
    return new Promise(function (fulfill, reject) {
      fetch(options, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      }, reject)
    })
  },
  deleteComputedDatapoint (computedId) {
    let fetch = api.endPoint('/computed_datapoint/' + computedId, 'delete', 1)
    return new Promise(function (fulfill, reject) {
      fetch(null, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      }, reject)
    })
  }
}

// deleteChart (id) {
//   let fetch = api.endPoint('/custom_chart/' + id, 'delete', 1)
//   return new Promise(function (fulfill, reject) {
//     fetch(null, null, {'cache-control': 'no-cache'}).then(function (chart) {
//       fulfill(chart)
//     })
//   })
// }
