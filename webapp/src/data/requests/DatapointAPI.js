import api from 'data/api'

export default {
  getFilteredDatapoints (options) {
    let fetch = api.endPoint('/datapoint/')
    return new Promise(function (fulfill, reject) {
      fetch(options, null, {'cache-control': 'no-cache'}).then(function (datapoint) {
        fulfill(datapoint)
      })
    })
  }
}
