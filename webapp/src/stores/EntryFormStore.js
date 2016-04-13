import _ from 'lodash'
import Reflux from 'reflux'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'
import flattenChildren from 'data/transform/flattenChildren'
import api from 'data/api'
import DatapointAPI from 'data/requests/DatapointAPI'

let EntryFormStore = Reflux.createStore({
  listenables: [require('actions/EntryFormActions')],
  locationList: [],

  data: {
    apiResponseData: null,
    indicatorMap: null,
    indicatorsToTags: [],
    filteredIndicators: [],
    data: null,
    loaded: false,
    campaigns: [],
    campaignNames: [],
    couldLoad: false,
    filterLocations: [],
    locationMap: null,
    locationSelected: [],
    locations: [],
    sourceList: [],
    selected: {
      form: { title: 'Select Form', value: null },
      campaign: { title: 'Select Campaign', value: null },
      source: { title: 'Select Source', value: null },
      locations: []
    },
    tags: [],
    tagNames: [],
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

    Promise.all([
      api.get_indicator_tag({'show_leaf': 1}, null, {'cache-control': 'no-cache'}),
      api.indicator_to_tag(),
      api.campaign(null, null, {'cache-control': 'no-cache'}),
      api.locations(),
      api.indicators({ read_write: 'w' }, null, {'cache-control': 'no-cache'})])
      .then(_.spread(function (tags, indicatorToTags, campaigns, locations, indicators) {
        let indicatorToTagsResult = _(indicatorToTags.objects)
          .map(indToTag => {
            return {
              'id': indToTag.id,
              'value': indToTag.indicator_tag_id,
              'name': indToTag.indicator__short_name,
              'title': indToTag.indicator_tag__tag_name
            }
          }).value()

        self.data.indicatorsToTags = indicatorToTagsResult
        let tagResult = _(tags.objects)
          .map(tag => {
            return {
              'value': tag.id,
              'title': tag.tag_name
            }
          }).value()
        self.data.tags = tagResult
        self.data.tagNames = _(tags.objects)
          .map(tag => {
            return tag.tag_name
          }).value()

        let campaignResult = _(campaigns.objects)
          .map(campaign => {
            return {
              'id': campaign.id,
              'name': campaign.name
            }
          }).value()
        self.data.campaigns = campaignResult
        // map names
        self.data.campaignNames = _(campaigns.objects)
          .map(campaign => {
            return campaign.name
          }).value()
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

        // Sources

        self.data.sourceList = [
          {'id': 1, 'title': 'PEMT'},
          {'id': 2, 'title': 'ICM'},
          {'id': 3, 'title': 'PEMT / DMT'},
          {'id': 4, 'title': 'District Team'},
          {'id': 5, 'title': 'UNICEF'},
          {'id': 6, 'title': 'AFP'},
          {'id': 7, 'title': 'Provincial Governors Office'},
          {'id': 8, 'title': 'PEMT / WHO / UNICEF'},
          {'id': 9, 'title': 'Joint Access reports'},
          {'id': 10, 'title': 'Finger Mark Survey'},
          {'id': 11, 'title': 'PEMT/WHO/UNICEF'},
          {'id': 12, 'title': 'DMT'},
          {'id': 13, 'title': 'PCA'}
        ]

        self.trigger(self.data)
      })
    )
  },

  _setCouldLoad: function () {
    this.data.couldLoad = (this.data.selected.form.value !== null &&
      this.data.selected.campaign.value !== null &&
      this.data.locationSelected.length > 0)
    if (this.data.couldLoad) { this._getTableData() }
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

  onSetForm: function (formValue) {
    this.data.selected.form.value = formValue
    this.data.selected.form.title = this.data.tagNames[formValue - 1]
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onSetCampaign: function (campaignId) {
    this.data.selected.campaign.value = campaignId
    this.data.selected.campaign.title = this.data.campaignNames[campaignId - 1]
    this._setCouldLoad()
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
  _filterIndicators: function () {
    this.data.filteredIndicators = []
    this.data.indicatorsToTags.forEach(indicator => {
      if (indicator.title === this.data.selected.form.title) {
        this.data.filteredIndicators.push(this.data.indicatorMap[indicator.id])
      }
    })
    this.trigger(this.data)
  },

  _getIndicatorIds: function () {
    return this.data.filteredIndicators.map(function (indicator) {
      return indicator.id
    })
  },

  _getTableData: function () {
    this._filterIndicators()
    let options = {
      campaign__in: parseInt(this.data.selected.campaign.value, 10),
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

    options.indicator__in = this._getIndicatorIds()

    _.defaults(options, this.data.pagination)

    this.data.loaded = false
    this.trigger(this.data)
    DatapointAPI.getFilteredDatapoints(options, null, {'cache-control': 'no-cache'}).then(response => {
      this.data.loaded = true
      this.data.apiResponseData = response.objects
      this.trigger(this.data)
    }, function (err) {
      console.error(err)
      this.data.loaded = false
      this.trigger(this.data)
    })
  }
})

export default EntryFormStore
