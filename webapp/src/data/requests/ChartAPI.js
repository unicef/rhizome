import _ from 'lodash'
import api from 'data/api'

export default {
  getCharts () {
    return api.get_chart(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _(response.objects).sortBy('id').reverse().value()
    })
  },

  getChart (id) {
    let fetch = api.endPoint('/custom_chart/' + id, 'get', 1)
    return new Promise(function (fulfill, reject) {
      fetch(null, null, {'cache-control': 'no-cache'}).then(function (chart) {
        fulfill(chart.objects)
      })
    })
  }
}
