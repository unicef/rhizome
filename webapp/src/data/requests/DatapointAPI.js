import api from 'data/api'

export default {
  getFilteredDatapoints (options) {
    let fetch = api.endPoint('/datapoint/', 'get', 1)
    return new Promise(function (fulfill, reject) {
      fetch(options, null, {'cache-control': 'no-cache'}).then(function (datapoint) {
        fulfill(datapoint)
      })
    })
  }
}
