import _ from 'lodash'
import Reflux from 'reflux'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'
import api from 'data/api'

let EntryFormStore = Reflux.createStore({
  listenables: [require('actions/EntryFormActions')],

  data: {
    indicator_set_id: 2,
    campaigns: [],
    campaign_id: null,
    couldLoad: false,
    locations: [],
    locationMap: [],
    locationSelected: []
  },

  getInitialState: function () {
    return this.data
  },

  onGetCampaigns: function () {
    api.campaign(null, null, {'cache-control': 'no-cache'})
      .then(response => {
        let campains
        if (!response.objects) {
          campains = null
        } else {
          campains = response.objects.sort(function (a, b) {
            if (a.office === b.office) {
              return a.start_date > b.start_data ? -1 : 1
            }
            return a.office - b.office
          })
          .map(function (d) {
            d.text = d.name
            d.value = d.id
            return d
          })
        }
        this.data.campaigns = campains
        this.data.campaign_id = this.data.campaigns[0].value
        this.trigger(this.data)
      })
  },

  onGetLocations: function () {
    api.locations()
      .then(response => {
        let locations = _(response.objects)
          .map(location => {
            return {
              'title': location.name,
              'value': location.id,
              'parent': location.parent_location_id
            }
          })
          .sortBy('title')
          .reverse()
          .thru(_.curryRight(treeify)('value'))
          .map(ancestryString)
          .value()

        this.data.locations = locations

        this.data.locationMap = _.indexBy(response.objects, 'id')
        this.trigger(this.data)
      })
  },

  _setCouldLoad: function () {
    this.data.couldLoad = this.data.locationSelected.length > 0
  },

  onSetIndicator: function (optionId) {
    this.data.indicator_set_id = optionId
    this.trigger(this.data)
  },

  onSetCampaign: function (campaignId) {
    this.data.campaign_id = campaignId
    this.trigger(this.data)
  },

  onAddLocations: function (id) {
    this.data.locationSelected.push(this.data.locationMap[id])
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onRemoveLocation: function (id) {
    _.remove(this.data.locationSelected, {id: id})
    this._setCouldLoad()
    this.trigger(this.data)
  }
})

export default EntryFormStore
