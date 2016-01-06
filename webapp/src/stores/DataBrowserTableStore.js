import Reflux from 'reflux'
import parseSchema from 'ufadmin/utils/parseSchema'

import _ from 'lodash'
import moment from 'moment'
import api from 'data/api'

var DataBrowserTableStore = Reflux.createStore({
  listenables: [require('actions/DataBrowserTableActions')],

  data: {
    data: null,
    schema: null,
    fields: null
  },

  getInitialState: function () {
    return this.data
  },

  onGetTableData: function (options, columns) {
    api.datapoints(options, null, {'cache-control': 'no-cache'})
      .then(response => {
        if (!response.objects || response.objects.length < 1) {
          this.data.data = null
          this.trigger(this.data)
          return
        }

        var value = response.objects.map(function (item) {
          var result = _.pick(item, 'location')
          result.campaign = moment(item.campaign.start_date).format('MMM YYYY')

          item.indicators.forEach(function (indicator) {
            result['indicators'] = indicator.value
          })
          return result
        })

        this.data.data = value
        this.data.schema = parseSchema(response)
        this.data.fields = ['location', 'campaign', 'indicators'] || columns

        this.trigger(this.data)
      })
  }
})

export default DataBrowserTableStore
