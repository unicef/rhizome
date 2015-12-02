import _ from 'lodash'
import Reflux from 'reflux'

import api from 'data/api'

var IndicatorStore = Reflux.createStore({

  init: function () {
    this.indicators = []
    this.indicatorsPromise =
      api.indicators(null, null, {'cache-control': 'no-cache'}).then(function (response) {
        var indicators = response.objects
        this.indicators = _.indexBy(indicators, 'id')

        this.trigger({ indicators: indicators })

        return this.indicators
      }.bind(this))
  },

  getInitialState: function () {
    return {
      indicators: this.indicators
    }
  },

  getById: function (indicators) {
    return indicators.map(id => this.indicators[id])
  },

  getIndicatorsPromise: function () {
    return this.indicatorsPromise
  }
})

export default IndicatorStore
