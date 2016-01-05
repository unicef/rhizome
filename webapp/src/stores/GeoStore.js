import Reflux from 'reflux'
import _ from 'lodash'

import api from 'data/api'

var GeoStore = Reflux.createStore({
  listenables: [require('actions/GeoActions')],

  init: function () {
    this.location = null
    this.features = []
  },

  onFetch: function (location) {
    this.location = location
    api.geo({ parent_location_id__in: location.id }, null, {'cache-control': 'max-age=604800, public'}).then(this.loadGeography)
  },

  loadGeography: function (response) {
    this.features = _(response.objects.features).flatten().value()
    this.trigger({
      features: this.features
    })
  }
})

export default GeoStore
