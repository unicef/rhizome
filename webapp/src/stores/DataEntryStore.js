import _ from 'lodash'
import Reflux from 'reflux'

import api from 'data/api'
import DatapointAPI from 'data/requests/DatapointAPI'

let DataEntryStore = Reflux.createStore({

  listenables: [require('actions/DataEntryActions')],

  data: {
    table_data: null,
    selected_campaign: null,
    selected_indicator_tag: null,
    selected_indicators: [],
    selected_locations: [],
    selected_source: null,
    indicators_to_tags: [],
    sources: [
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
  },

  getInitialState: function () {
    return this.data
  },

  init: function () {
    let self = this
    Promise.resolve(api.indicator_to_tag()).then(indicator_to_tags => {
      self.data.indicators_to_tags = indicator_to_tags.objects
      self.trigger(self.data)
    })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSetIndicatorsByTag: function (indicator_tag, indicators_index) {
    this.data.selected_indicator_tag = indicator_tag
    this.data.selected_indicators = []
    this.data.indicators_to_tags.forEach(indicator_to_tag => {
      if (indicator_to_tag.indicator_tag_id === indicator_tag.id) {
        this.data.selected_indicators.push(indicators_index[indicator_to_tag.indicator_id])
      }
    })
    this.data.table_data = null
    this.updateTable()
  },

  onSetCampaign: function (campaign) {
    this.data.selected_campaign = campaign
    this.data.table_data = null
    this.updateTable()
  },

  onAddLocation: function (location) {
    this.data.selected_locations.push(location)
    this.updateTable()
  },

  onRemoveLocation: function (id) {
    _.remove(this.data.selected_locations, {id: id})
    this.updateTable()
  },

  onSetSource: function (sourceId) {
    this.data.selected_source.value = sourceId
    this.data.selected_source.title = _.filter(this.data.sources, { value: sourceId })[0].title
    this.updateTable()
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  updateTable: function () {
    this.data.table_data = null
    const d = this.data
    if (d.selected_indicator_tag && d.selected_campaign && d.selected_locations.length > 0) {
      this.getTableData()
    }
    this.trigger(this.data)
  },

  getTableData: function () {
    const options = {
      campaign__in: parseInt(this.data.selected_campaign.id, 10),
      indicator__in: this.data.selected_indicators.map(indicator => indicator.id),
      location_id__in: this.data.selected_locations.map(location => location.id),
      show_missing_data: 1,
      source_name: ''
    }

    DatapointAPI.getFilteredDatapoints(options, null, {'cache-control': 'no-cache'}).then(response => {
      const campaign_index = _.indexBy(response.meta.campaign_list, 'id')
      this.data.table_data = response.objects.map(datapoint => {
        return {
          'campaign': campaign_index[datapoint.campaign],
          'location': datapoint.location,
          'indicators': datapoint.indicators
        }
      })
      this.trigger(this.data)
    }, function (err) {
      console.error(err)
      this.trigger(this.data)
    })
  }
})

export default DataEntryStore
