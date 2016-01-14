import _ from 'lodash'
import Reflux from 'reflux'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'
import flattenChildren from 'data/transform/flattenChildren'
import api from 'data/api'

let EntryFormStore = Reflux.createStore({
  listenables: [require('actions/EntryFormActions')],

  locations: [],

  data: {
    indicatorSelected: '2',
    campaigns: [],
    campaignSelected: null,
    couldLoad: false,
    filterLocations: [],
    locationMap: [],
    locationSelected: [],
    includeSublocations: false
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
        this.data.campaignSelected = this.data.campaigns[0].value
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

        this.locations = locations
        this.data.filterLocations = locations
        this._filterLocationsByCampaign()
        this.data.locationMap = _.indexBy(response.objects, 'id')
        this.trigger(this.data)
      })
  },

  _setCouldLoad: function () {
    this.data.couldLoad = this.data.locationSelected.length > 0
  },

  _filterLocationsByCampaign: function () {
    let campaign = _(this.data.campaigns).find(campaign => {
      return campaign.id === parseInt(this.data.campaignSelected, 10)
    })

    this.data.filterLocations = this.locations.filter(location => {
      return location.value === campaign.office_id
    })
  },

  onChangeSelect: function () {
    if (this.data.includeSublocations) {
      this.data.includeSublocations = false
    } else {
      this.data.includeSublocations = true
    }
    this.trigger(this.data)
  },

  onSetIndicator: function (indicatorId) {
    this.data.indicatorSelected = indicatorId
    this.trigger(this.data)
  },

  onSetCampaign: function (campaignId) {
    this.data.campaignSelected = campaignId
    this._filterLocationsByCampaign()
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
  },

  onGetTableData: function (indicatorSet, indicatorSelected, campaignSelected, locationSelected) {
    let options = {
      campaign__in: parseInt(this.data.campaignSelected, 10),
      indicator__in: [],
      location_id__in: []
    }

    if (locationSelected.length > 0) {
      options.location_id__in = _.map(locationSelected, 'id')

      _.forEach(locationSelected, location => {
        if (this.data.includeSublocations) {
          let parentLocations = this._findLocationObject(this.locations, location.id)

          let children = flattenChildren(parentLocations, 'children', null, function () { return true }, 1)
          if (children.length > 0) {
            options.location_id__in = options.location_id__in.concat(_.map(children, 'value'))
          }
        }
      })
      options.location_id__in = _.uniq(options.location_id__in)
    }

    _.forEach(indicatorSet, function (indicator) {
      if (indicator.id.toString() === indicatorSelected) {
        options.indicator__in = _.compact(_.map(indicator.indicators, 'id'))
      }
    })

    api.datapointsRaw(options, null, {'cache-control': 'no-cache'})
  },

  _findLocationObject: function (locations, locationId) {
    return _.find(locations, location => {
      return location.value === locationId
        ? location : !location.children && location.children.length > 0
        ? this._filterLocationsByCampaign(location.children, locationId) : []
    })
  }
})

export default EntryFormStore
