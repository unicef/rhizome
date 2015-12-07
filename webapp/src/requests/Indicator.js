import _ from 'lodash'
import api from 'data/api'

export default {
  getIndicators () {
    return api.indicators(null, null, { 'cache-control': 'max-age=86400, public' }).then(response => {
      return _.indexBy(response.objects, 'id')
    })
  }
}
