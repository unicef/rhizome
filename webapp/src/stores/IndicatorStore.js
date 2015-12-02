import _ from 'lodash'
import Reflux from 'reflux'

import api from 'data/api'

var IndicatorStore = Reflux.createStore({

  getIndicators () {
    return api.indicators(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _.indexBy(response.objects, 'id')
    })
  },

  async getById (indicators) {
    let indicatorIndex = await this.getIndicators()
    return indicators.map(id => indicatorIndex[id])
  }
})

export default IndicatorStore
