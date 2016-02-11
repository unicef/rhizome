import _ from 'lodash'
import Reflux from 'reflux'
import api from 'data/api'
import Location from 'data/requests/Location'

import MapFormActions from 'actions/MapFormActions'
import CampaignStore from 'stores/CampaignStore'

var MapFormStore = Reflux.createStore({
  listenables: MapFormActions,
  data: {
    locations: null,
    locationsLoaded: false,
    campaigns: null,
    campaignsLoaded: false,
    indicators: null,
    indicatorsLoaded: false
  },

  getInitialState: function () {
    return this.data
  },

  onGetLocations: function () {
    if (!this.data.locationsLoaded) {
      this.data.locationsLoaded = true
      Promise.all([
        Location.getLocations(),
        Location.getLocationTypes()
      ])
      .then(([locations, locationsTypes]) => {
        var locationIdx = _.indexBy(locations, 'id')
        var types = _.indexBy(locationsTypes, 'id')
        locations.forEach(location => {
          location.location_type = _.get(types[location.location_type_id], 'name')
          location.parent = locationIdx[location.parent_location_id]
        })
        this.data.locations = locations
        this.trigger(this.data)
      })
    }
  },

  onGetCampaigns: function () {
    if (!this.data.campaignsLoaded) {
      this.data.campaignsLoaded = true
      CampaignStore.getCampaignsPromise()
        .then(campaigns => {
          this.data.campaigns = campaigns
          this.trigger(this.data)
        })
    }
  },

  onGetIndicators: function () {
    if (!this.data.indicatorsLoaded) {
      this.data.indicatorsLoaded = true
      api.indicatorsTree().then(indicators => {
        this.data.indicators = indicators.objects
        this.trigger(this.data)
      })
    }
  }
})

export default MapFormStore
