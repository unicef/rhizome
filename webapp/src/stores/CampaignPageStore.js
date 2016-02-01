import _ from 'lodash'
import Reflux from 'reflux'

import api from 'data/api'
import CampaignPageActions from 'actions/CampaignPageActions'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

let CampaignPageStore = Reflux.createStore({
  listenables: [CampaignPageActions],

  data: {
    offices: [],
    locations: [],
    locationMap: [],
    indicatorToTags: [],
    campaignTypes: [],
    campaign: {
      start: '',
      end: ''
    },
    campaignName: '',
    locationSelected: [],
    postData: {
      id: -1,
      campaign_type_id: '',
      name: '',
      office_id: '',
      top_lvl_indicator_tag_id: '',
      top_lvl_location_id: '',
      pct_complete: 0.001,
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
      api.office(),
      api.locations(),
      api.get_indicator_tag(),
      api.campaign_type(),
      id ? api.campaign({'id__in': id}, null, {'cache-control': 'no-cache'}) : []
    ]).then(_.spread(function (offices, locations, indicatorToTags, campaignTypes, campaign) {
      self.data.isLoaded = true
      var currentCampaign = campaign.objects ? campaign.objects[0] : ''
      self.data.offices = offices.objects
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
      self.data.campaignTypes = campaignTypes.objects
      if (currentCampaign) {
        self.data.postData = _.clone(currentCampaign)
        self.data.campaign.start = currentCampaign.start_date
        self.data.campaign.end = currentCampaign.end_date
        self.data.locationSelected[0] = self.data.locationMap[self.data.postData.top_lvl_location_id]
      } else {
        self.data.postData.id = -1
        self.data.postData.name = ''
        self.data.postData.campaign_type_id = self.data.campaignTypes ? self.data.campaignTypes[0].id : ''
        self.data.postData.office_id = self.data.offices ? self.data.offices[0].id : ''
        self.data.postData.top_lvl_indicator_tag_id = self.data.indicatorToTags ? self.data.indicatorToTags[0].id : ''
        self.data.postData.top_lvl_location_id = self.data.locations ? self.data.locations[0].id : ''
        self.data.postData.pct_complete = 0.001
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
  onSetOffice: function (officeId) {
    this.data.postData.office_id = officeId
    this.trigger(this.data)
  },
  onSetIndicatorTag: function (indicatorTagId) {
    this.data.postData.top_lvl_indicator_tag_id = indicatorTagId
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
  onSetLocation: function (locationId) {
    this.data.postData.top_lvl_location_id = locationId
    this.data.locationSelected[0] = this.data.locationMap[locationId]
    this.trigger(this.data)
  }
})

export default CampaignPageStore
