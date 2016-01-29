import _ from 'lodash'
import Reflux from 'reflux'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'
import flattenChildren from 'data/transform/flattenChildren'
import api from 'data/api'

import CampaignPageActions from 'actions/CampaignPageActions'

let CampaignPageStore = Reflux.createStore({
  listenables: [CampaignPageActions],

  data: {
    offices: [],
    locations: [],
    indicatorToTags: []
  },

  getInitialState: function () {
    return this.data
  },

  onInitData: function () {
    let self = this
    Promise.all([
      api.office(),
      api.locations(),
      api.get_indicator_tag()
    ]).then(_.spread(function (offices, locations, indicatorToTags) {
      self.data.offices = offices.objects
      self.data.locations = locations.objects
      self.data.indicatorToTags = indicatorToTags.objects
      self.trigger(self.data)
      }), function (error) {
      self.trigger(self.data)
    })
  }
})

export default CampaignPageStore
