import _ from 'lodash'
import api from 'data/api'

export default {
  getCampaigns () {
    return api.campaign(null, null, {'cache-control': 'no-cache'}).then(response => {
      return _(response.objects).sortBy('id').reverse().value()
    })
  },

  getCampaign (id) {
    let fetch = api.endPoint('/campaign/' + id, 'get', 1)
    return new Promise(function (fulfill, reject) {
      fetch(null, null, {'cache-control': 'no-cache'}).then(function (campaign) {
        fulfill(campaign.objects)
      })
    })
  }
}
