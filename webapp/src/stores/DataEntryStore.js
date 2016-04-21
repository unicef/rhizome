import _ from 'lodash'
import Reflux from 'reflux'
import DatapointActions from 'actions/DatapointActions'
import DataEntryActions from 'actions/DataEntryActions'

let DataEntryStore = Reflux.createStore({

  listenables: [DataEntryActions],

  data: {
    selected_campaign: null,
    selected_indicator_tag: null,
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

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSetIndicatorsByTag: function (indicator_tag, indicators_index) {
    this.data.selected_indicator_tag = indicator_tag
    this.updateTable()
  },

  onSetCampaign: function (campaign) {
    this.data.selected_campaign = campaign
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
    const d = this.data
    if (d.selected_indicator_tag && d.selected_campaign && d.selected_locations.length > 0) {
      DatapointActions.fetchDatapoints({
        campaign__in: parseInt(this.data.selected_campaign.id, 10),
        indicator_ids: this.data.selected_indicator_tag.indicators.map(indicator => indicator.id),
        location_ids: this.data.selected_locations.map(location => location.id),
        show_missing_data: 1,
        source_name: ''
      })
    }
    this.trigger(this.data)
  }
})

export default DataEntryStore
