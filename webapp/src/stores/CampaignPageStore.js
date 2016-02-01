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
    selectedOffice: [],
    selectedIndicatorTag: [],
    selectedLocation: [],
    selectedCampaignType: [],
    displayMsg: false,
    message: ''
  },

  getInitialState: function () {
    return this.data
  },

  onInitialize: function () {
    let self = this
    Promise.all([
      api.office(),
      api.locations(),
      api.get_indicator_tag(),
      api.campaign_type()
    ]).then(_.spread(function (offices, locations, indicatorToTags, campaignTypes) {
      self.data.offices = offices.objects
      self.data.locations = locations.objects
      self.data.indicatorToTags = indicatorToTags.objects
      self.data.campaignTypes = campaignTypes.objects
      self.data.selectedOffice = self.data.offices ? self.data.offices[0] : []
      self.data.selectedIndicatorTag = self.data.indicatorToTags ? self.data.indicatorToTags[0] : []
      self.data.selectedLocation = self.data.locations ? self.data.locations[0] : []
      self.data.selectedCampaignType = self.data.campaignTypes ? self.data.campaignTypes[0] : []
      self.trigger(self.data)
    }), function (error) {
      console.error(error)
      self.trigger(self.data)
    })
  },
  onSaveCampaign: function (postData) {
    let self = this
    console.log(postData)
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
    this.data.selectedOffice = officeId
    this.trigger(this.data)
  },
  onSetIndicatorTag: function (indicatorTagId) {
    this.data.selectedIndicatorTag = indicatorTagId
    this.trigger(this.data)
  },
  onSetCampaignType: function (campaignTypeId) {
    this.data.selectedCampaignType = campaignTypeId
    this.trigger(this.data)
  },
  onSetLocation: function (locationId) {
    this.data.selectedLocation = locationId
    this.trigger(this.data)
  },
  onSetCampaignName: function (name) {
    this.data.campaignName = name
    this.trigger(this.data)
  }
})

export default CampaignPageStore
