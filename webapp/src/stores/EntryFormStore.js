import Reflux from 'reflux'

import api from 'data/api'

let EntryFormStore = Reflux.createStore({
  listenables: [require('actions/EntryFormActions')],

  data: {
    indicator_set_id: 2,
    campaigns: [],
    campaign_id: null,
    campaign_office_id: null
  },

  getInitialState: function () {
    return this.data
  },

  onGetCampaigns: function () {
    api.campaign(null, null, {'cache-control': 'no-cache'})
      .then(response => {
        let campains
        if (!response.objects) {
          campains = null
        } else {
          campains = response.objects.sort(function (a, b) {
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
        this.data.campaigns = campains
        this.data.campaign_id = this.data.campaigns[0].value
        this.trigger(this.data)
      })
  },

  onSetIndicator: function (optionId) {
    this.data.indicator_set_id = optionId
    this.trigger(this.data)
  },

  onSetCampaign: function (campaignId) {
    this.data.campaign_id = campaignId
    this.trigger(this.data)
  }
})

export default EntryFormStore
