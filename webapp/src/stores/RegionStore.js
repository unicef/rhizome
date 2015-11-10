'use strict'

var Reflux = require('reflux')
var api = require('data/api')

var RegionStore = Reflux.createStore({
  init () {
    this.locations = []
    this.LocationTypes = []

    this.locationsPromise = api.locations()
      .then(data => {
        this.locations = data.objects
        this.trigger({
          locations: this.locations
        })
        return this.locations
      })

    this.LocationTypesPromise = api.location_type()
      .then(data => {
        this.LocationTypes = data.objects
        this.trigger({
          LocationTypes: this.LocationTypes
        })
        return this.LocationTypes
      })
  },

  getInitialState () {
    return {
      locations: this.locations,
      LocationTypes: this.LocationTypes
    }
  },

  // API
  getlocationsPromise () {
    return this.locationsPromise
  },

  getLocationTypesPromise () {
    return this.LocationTypesPromise
  }
})

module.exports = RegionStore
