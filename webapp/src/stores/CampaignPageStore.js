import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'

import api from 'utilities/api'
import CampaignPageActions from 'actions/CampaignPageActions'

import ancestryString from 'utilities/transform/ancestryString'
import treeify from 'utilities/transform/treeify'

let CampaignPageStore = Reflux.createStore({
  listenables: [CampaignPageActions],

  data: {
    locations: [],
    locationMap: [],
    indicatorToTags: [],
    campaignTypes: [],
    campaign: {
      start: '',
      end: ''
    },
    campaignName: '',
    postData: {
      campaign_type_id: '',
      name: '',
      start_date: '',
      end_date: ''
    },
    displayMsg: false,
    message: '',
    isLoaded: false,
    saveSuccess: false
  },

  getInitialState: function () {
    return this.data
  },

  onInitialize: function (id) {
    let self = this
    Promise.all([
      api.locations(),
      api.tagTree(),
      api.get_indicator_tag(),
      api.campaign_type(),
      id ? api.campaign({'id__in': id}, null, {'cache-control': 'no-cache'}) : []
    ]).then(_.spread(function (locations, indicatorToTags, allTags, campaignTypes, campaign) {
      self.data.isLoaded = true
      var currentCampaign = campaign.objects ? campaign.objects[0] : null
      self.data.locations = _(locations.objects)
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
      self.data.locationMap = _.indexBy(locations.objects, 'id')
      self.data.indicatorToTags = indicatorToTags.objects
      self.data.tagMap = _.indexBy(allTags.objects, 'id')
      self.data.campaignTypes = campaignTypes.objects
      if (currentCampaign) {
        self.data.postData = _.clone(currentCampaign)
        self.data.campaign.start = moment(currentCampaign.start_date).toDate()
        self.data.campaign.end = moment(currentCampaign.end_date).toDate()
      } else {
        self.data.postData.name = ''
        self.data.postData.campaign_type_id = self.data.campaignTypes ? self.data.campaignTypes[0].id : ''
        self.data.campaign.start = new Date()
        self.data.campaign.end = new Date()
      }
      self.trigger(self.data)
    }), function () {
      self.data.isLoaded = true
      self.trigger(self.data)
    })
  },
  onSaveCampaign: function (postData) {
    let self = this
    Promise.all([api.post_campaign(postData)]).then(_.spread(function (response) {
      self.data.campaignName = response.objects.name
      self.data.displayMsg = true
      self.data.saveSuccess = true
      self.data.message = postData.id === -1 ? 'Campaign is successfully created.' : 'Campaign is updated successfully.'
      self.trigger(self.data)
    }), function (error) {
      self.data.campaignName = postData.name
      self.data.displayMsg = true
      self.data.saveSuccess = false
      self.data.message = error.msg
      self.trigger(self.data)
    })
  },
  onUpdateCampaignRange: function (key, value) {
    this.data.campaign[key] = value
    this.trigger(this.data)
  },
  onSetCampaignType: function (campaignTypeId) {
    this.data.postData.campaign_type_id = campaignTypeId
    this.trigger(this.data)
  },
  onSetCampaignName: function (name) {
    this.data.postData.name = name
    this.trigger(this.data)
  },
})

export default CampaignPageStore
