import _ from 'lodash'
import Reflux from 'reflux'

import api from 'data/api'
import CampaignPageActions from 'actions/CampaignPageActions'

let CampaignPageStore = Reflux.createStore({
  listenables: [CampaignPageActions],

  data: {
    offices: [],
    locations: [],
    indicatorToTags: [],
    campaignTypes: [],
    campaign: {
      start: '',
      end: ''
    },
    campaignName: '',
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
    message: ''
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
      id ? api.campaign({'id__in': id}) : []
    ]).then(_.spread(function (offices, locations, indicatorToTags, campaignTypes, campaign) {
      var currentCampaign = campaign.objects ? campaign.objects[0] : ''
      self.data.offices = offices.objects
      self.data.locations = locations.objects
      self.data.indicatorToTags = indicatorToTags.objects
      self.data.campaignTypes = campaignTypes.objects
      if (currentCampaign) {
        self.data.postData = _.clone(currentCampaign)
        self.data.campaign.start = currentCampaign.start_date
        self.data.campaign.end = currentCampaign.end_date
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
    }), function (error) {
      console.error(error)
      self.trigger(self.data)
    })
  },
  onSaveCampaign: function (postData) {
    let self = this
    Promise.all([api.post_campaign(postData)]).then(_.spread(function (response) {
      self.data.campaignName = response.objects.name
      self.data.displayMsg = true
      self.data.message = 'Campaign is successfully created.'
      self.trigger(self.data)
    }), function (error) {
      self.data.campaignName = postData.name
      self.data.displayMsg = true
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
  onSetLocation: function (locationId) {
    this.data.postData.top_lvl_location_id = locationId
    this.trigger(this.data)
  },
  onSetCampaignName: function (name) {
    this.data.postData.name = name
    this.trigger(this.data)
  }
})

export default CampaignPageStore
