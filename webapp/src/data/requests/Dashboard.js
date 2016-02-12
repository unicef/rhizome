import _ from 'lodash'
import api from 'data/api'

export default {
  getDashboards () {
    return api.get_dashboard(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _(response.objects).sortBy('id').reverse().value()
    })
  }
}
