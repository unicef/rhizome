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
    indicatorSets: require('./IndicatorSets'),
    indicatorMap: null,
    data: null,
    loaded: false,
    indicatorSelected: '2',
    campaigns: [],
    campaignSelected: null,
    couldLoad: false,
    filterLocations: [],
    locationMap: null,
    locationSelected: [],
    includeSublocations: false,
    indicatorSet: null,
    pagination: {
      total_count: 0
    }
  },

  getInitialState: function () {
    return this.data
  },

  onInitData: function () {
    let self = this
    Promise.all([api.campaign(null, null, {'cache-control': 'no-cache'}),
      api.locations(),
      api.indicators({ read_write: 'w' }, null, {'cache-control': 'no-cache'})]).then(_.spread(function (campaigns, locations, indicators) {
        // campains
        let campainResult
        if (!campaigns.objects) {
          campainResult = null
        } else {
          campainResult = campaigns.objects.sort(function (a, b) {
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
        self.data.campaigns = campainResult
        self.data.campaignSelected = campainResult[0].value

        // locations
        let locationResult = _(locations.objects)
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

        self.locations = locationResult
        self.data.filterLocations = locationResult
        self.data.locationMap = _.indexBy(locations.objects, 'id')

        // Indicators
        self.data.indicators = _.indexBy(indicators.objects, 'id')
        self.trigger(self.data)
      })
    )
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

  onGetTableData: function () {
    let options = {
      campaign__in: parseInt(this.data.campaignSelected, 10),
      indicator__in: [],
      location_id__in: []
    }

    if (this.data.locationSelected.length > 0) {
      options.location_id__in = _.map(this.data.locationSelected, 'id')

      _.forEach(this.data.locationSelected, location => {
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

    _.forEach(this.data.indicatorSets, indicator => {
      if (indicator.id.toString() === this.data.indicatorSelected) {
        this.data.indicatorSet = indicator
        options.indicator__in = _.compact(_.map(indicator.indicators, 'id'))
      }
    })

    _.defaults(options, this.data.pagination)

    api.datapointsRaw(options, null, {'cache-control': 'no-cache'}).then(response => {
      this.data.loaded = true
      this.data.data = response.objects
      this.trigger(this.data)
    })
  },

  _findLocationObject: function (locations, locationId) {
    return _.find(locations, location => {
      return location.value === locationId
        ? location : !location.children && location.children.length > 0
        ? this._findLocationObject(location.children, locationId) : []
    })
  }
})

export default EntryFormStore
