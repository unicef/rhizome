import Reflux from 'reflux'
import api from 'data/api'

var CampaignStore = Reflux.createStore({
  init () {
    this.campaigns = []

    this.campaignsPromise = api.campaign()
      .then(data => {
        this.campaigns = data.objects
        this.trigger({
          campaigns: this.campaigns
        })
        return this.campaigns
      })
  },

  getInitialState () {
    return {
      campaigns: this.campaigns
    }
  },

  // API
  getCampaignsPromise () {
    return this.campaignsPromise
  }
})

export default CampaignStore
