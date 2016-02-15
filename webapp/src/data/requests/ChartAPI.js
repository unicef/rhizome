import _ from 'lodash'
import api from 'data/api'

export default {
  getCharts () {
    return api.get_chart(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _(response.objects).sortBy('id').reverse().value()
    })
  }
}
