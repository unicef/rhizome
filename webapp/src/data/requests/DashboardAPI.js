import _ from 'lodash'
import api from 'data/api'

export default {
  getDashboards () {
    return api.get_dashboard(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _(response.objects).sortBy('id').reverse().value()
    })
  },

  getDashboard (id) {
    let fetch = api.endPoint('/custom_dashboard/' + id, 'get', 1)
    return new Promise(function (fulfill, reject) {
      fetch(null, null, {'cache-control': 'no-cache'}).then(function (dashboard) {
        fulfill(dashboard.objects)
      })
    })
  }
}
