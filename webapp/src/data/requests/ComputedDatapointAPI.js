import api from 'data/api'

export default {
  putComputedDatapoint (options) {
    let fetch = api.endPoint('/computed_datapoint/', 'put', 1)
    return new Promise(function (fulfill, reject) {
      fetch(options, null, {'cache-control': 'no-cache'}).then(function (response) {
        fulfill(response)
      })
    })
  }
}
