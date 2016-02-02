import Reflux from 'reflux'
import parseSchema from 'ufadmin/utils/parseSchema'
import d3 from 'd3'

import _ from 'lodash'
import moment from 'moment'
import api from 'data/api'

var DataBrowserTableStore = Reflux.createStore({
  listenables: [require('actions/DataBrowserTableActions')],

  data: {
    data: null,
    schema: null,
    fields: null,
    columns: null
  },

  getInitialState: function () {
    return this.data
  },

  _format: function (value) {
    if (_.isFinite(value)) {
      var format = d3.format('n')
      if (Math.abs(value) < 1 && value !== 0) {
        format = d3.format('.4f')
      }
      return format(value)
    }
    return ''
  },

  _buildSchema: function (schema, fields) {
    schema.items.properties = fields
    return schema
  },

  onGetTableData: function (campaign, locations, indicators) {
    this.data.data = null
    this.trigger(this.data)

    let fields = {location: {title: 'Location', name: 'location'}, campaign: {title: 'Campaign', name: 'campaign'}}
    let columns = ['location', 'campaign']
    let options = {indicator__in: []}

    if (locations.length > 0) {
      options.location__in = _.map(locations, 'id')
    }

    if (campaign.start) {
      options.campaign_start = moment(campaign.start).format('YYYY-M-D')
    }

    if (campaign.end) {
      options.campaign_end = moment(campaign.end).format('YYYY-M-D')
    }

    indicators.forEach(indicator => {
      options.indicator__in.push(indicator.id)
      fields[indicator.id] = {title: indicator.name, name: indicator.id}
      columns.push(indicator.id)
    })

    api.datapoints(options, null, {'cache-control': 'no-cache'})
      .then(response => {
        if (!response.objects || response.objects.length < 1) {
          this.data.data = null
          this.trigger(this.data)
          return
        }

        let value = response.objects.map(item => {
          let result = _.pick(item, 'location')
          result.campaign = moment(item.campaign.start_date).format('MMM YYYY')

          item.indicators.forEach(indicator => {
            result[indicator.indicator] = this._format(indicator.value)
          })
          return result
        })

        let pickValue = []
        _.forEach(value, item => {
          _.forEach(locations, location => {
            if (item.location === location.id) {
              item.location = location.name
              pickValue.push(item)
              return
            }
          })
        })

        this.data.data = pickValue
        this.data.schema = this._buildSchema(parseSchema(response), fields)
        this.data.fields = fields
        this.data.columns = columns

        this.trigger(this.data)
      })
  }
})

export default DataBrowserTableStore
