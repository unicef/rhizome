'use strict'

var Reflux = require('reflux')
var _ = require('lodash')

var api = require('data/api')

var GeoStore = Reflux.createStore({
  listenables: [require('actions/GeoActions')],

  init: function () {
    this.location = null
    this.features = []
  },

  onFetch: function (location) {
    this.location = location
    api.geo({ parent_location__in: location.id }).then(this.loadGeography)
  },

  loadGeography: function (response) {
    this.features = _(response.objects.features).flatten().value()
    // var border = _.find(this.features, f => f.properties.location_id === this.location.id)

    // console.log('border', border)
    // console.log('LOGGING THIS LOCATION: ', this.location.id)
    // console.log('LENGTH OF FEATURES: ', this.features.length)

    // border.properties.isBorder = true
    this.trigger({
      features: this.features
    })
  }
})

module.exports = GeoStore
