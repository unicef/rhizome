import _ from 'lodash'
import Reflux from 'reflux'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'
import flattenChildren from 'data/transform/flattenChildren'
import api from 'data/api'

let EntryFormStore = Reflux.createStore({
  listenables: [require('actions/EntryFormActions')],
  locationList: [],

  data: {
    indicatorSets: require('./IndicatorSets'),
    indicatorMap: null,
    indicatorSet: null,
    indicatorSelected: '2',
    data: null,
    loaded: false,
    campaigns: [],
    campaignSelected: null,
    couldLoad: false,
    filterLocations: [],
    locationMap: null,
    locationSelected: [],
    locations: [],
    includeSublocations: false,
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

        self.locationList = locationResult
        self.data.filterLocations = locationResult
        self.data.locationMap = _.indexBy(locations.objects, 'id')

        // Indicators
        self.data.indicatorMap = _.indexBy(indicators.objects, 'id')
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

    this.data.filterLocations = this.locationList.filter(location => {
      return location.value === campaign.office_id
    })
  },

  _filteredIndicatorSet: function (indicatorSetId) {
    var indicatorSet = _.find(this.data.indicatorSets, function (d) { return d.id === parseInt(indicatorSetId, 10) })
    if (!indicatorSet) return null

    var filtered = _.clone(indicatorSet)
    filtered.indicators = []
    _.each(indicatorSet.indicators, row => {
      if (row.type === 'section-header') { // header
        // remove previous section header if no indicators are included under it
        if (filtered.indicators.length > 0 && filtered.indicators[filtered.indicators.length - 1].type === 'section-header') {
          filtered.indicators.splice(filtered.indicators.length - 1, 1)
        }
        filtered.indicators.push(row)
      } else { // indicator
        // filter out indicators the user cannot edit
        if (row.id && this.data.indicatorMap[row.id] !== undefined) {
          row.name = this.data.indicatorMap[row.id].name
          filtered.indicators.push(row)
        }
      }
    })

    // remove last row if empty section header
    if (filtered.indicators[filtered.indicators.length - 1].type === 'section-header') {
      filtered.indicators.pop()
    }

    return filtered
  },

  _findLocationObject: function (locations, locationId) {
    return _.find(locations, location => {
      return location.value === locationId
        ? location : !location.children && location.children.length > 0
        ? this._findLocationObject(location.children, locationId) : []
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
          let parentLocations = this._findLocationObject(this.locationList, location.id)

          let children = flattenChildren(parentLocations, 'children', null, function () { return true }, 1)
          if (children.length > 0) {
            options.location_id__in = options.location_id__in.concat(_.map(children, 'value'))
          }
        }
      })
      options.location_id__in = _.uniq(options.location_id__in)

      // sort locations
      options.location_id__in = options.location_id__in.sort((a, b) => {
        var ra = this.data.locationMap[a]
        var rb = this.data.locationMap[b]
        // sort by location type first
        if (ra.location_type_id !== rb.location_type_id) {
          return ra.location_type_id - rb.location_type_id
        } else {
          return ra.name > rb.name ? 1 : -1
        }
      })

      this.data.locations = options.location_id__in
    }

    this.data.indicatorSet = this._filteredIndicatorSet(this.data.indicatorSelected)

    options.indicator__in = _(this.data.indicatorSet.indicators)
                  .filter(function (d) { return d.id })
                  .map(function (d) { return d.id })
                  .value()

    _.defaults(options, this.data.pagination)

    this.data.loaded = false
    this.trigger(this.data)

    api.datapointsRaw(options, null, {'cache-control': 'no-cache'}).then(response => {
      this.data.loaded = true
      this.data.data = response.objects
      this.trigger(this.data)
    }, function (err) {
      this.data.loaded = false
      console.error(err)
    })
  }
})

export default EntryFormStore
