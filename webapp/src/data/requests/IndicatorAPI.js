import _ from 'lodash'
import api from 'data/api'

export default {
  getIndicators () {
    return api.indicators(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _(response.objects).sortBy('id').reverse().value()
    }).then(error => { return error })
  }
}
