import Reflux from 'reflux'
import api from 'data/api'

var MapFormStore = Reflux.createStore({

  getSourceMap: function (id) {
    return api.get_source_object_map(id, null, {'cache-control': 'no-cache'})
      .then(function (response) {
        return response.objects[0]
      })
  },

  updateMetaMap: function (info) {
    return api.post_source_object_map(info).then(function (response) {
      return response.objects
    })
  },

  getIndicators: function () {
    return api.indicatorsTree().then(indicators => {
      return indicators.objects
    })
  }
})

export default MapFormStore
