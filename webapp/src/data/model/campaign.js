import _ from 'lodash'
import moment from 'moment'
import api from '../api'

function campaign (obj) {
  return obj
    ? update({}, obj)
    : {
      id: null,
      created_at: null,
      start_date: null,
      end_date: null,
      name: null,
      slug: null,
      resource_uri: null
    }
}

function update (campaign, obj) {
  _.assign(campaign, _.omit(obj, 'created_at', 'start_date', 'end_date'))

  campaign.created_at = moment(obj.created_at).toDate()
  campaign.start_date = moment(obj.start_date, 'YYYY-MM-DD').toDate()
  campaign.end_date = moment(obj.end_date, 'YYYY-MM-DD').toDate()

  return campaign
}

export default campaign
