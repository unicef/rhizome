import _ from 'lodash'
import api from 'data/api'

export default {
  getIndicators () {
    return api.indicators(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _.indexBy(response.objects, 'id')
    })
  },

  async getById (indicators) {
    let indicatorIndex = await this.getIndicators()
    return indicators.map(id => indicatorIndex[id])
  }
}
