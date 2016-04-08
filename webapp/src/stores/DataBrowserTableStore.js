import Reflux from 'reflux'
import parseSchema from 'components/organisms/manage-system/utils/parseSchema'
import d3 from 'd3'

import _ from 'lodash'
import moment from 'moment'

var DataBrowserTableStore = Reflux.createStore({
  listenables: [require('actions/DataBrowserTableActions')],

  table: {
    data: null,
    schema: null,
    fields: null,
    columns: null
  },

  getInitialState: function () {
    return this.table
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

  _extractItemsFromData: function (datapoints) {
    return datapoints.map(item => {
      let result = _.pick(item, 'location')
      result.campaign = moment(item.campaign.start_date).format('MMM YYYY')
      result.location_id = item.location
      result.campaign_id = item.campaign
      item.indicators.forEach(indicator => {
        // result[indicator.indicator] = this._format(indicator.value) // indicator.indicator is the id
        result[indicator.indicator] = {
          value: this._format(indicator.value), // indicator.indicator is the id
          computed: indicator.computed
        }
      })
      return result
    })
  },

  _getPickValue: function (items, locations) {
    let pickValue = []
    items.forEach(item => {
      locations.forEach(location => {
        if (item.location === location.id) {
          item.location = location.name
          pickValue.push(item)
          return
        }
      })
    })
    return pickValue
  },

  onGetTableData: function (locations, indicators, datapoints) {
    let fields = {location: {title: 'Location', name: 'location'}, campaign: {title: 'Campaign', name: 'campaign'}}
    let columns = ['location', 'campaign']
    let items = this._extractItemsFromData(datapoints)
    indicators.forEach(indicator => {
      fields[indicator.id] = {title: indicator.name, name: indicator.id, 'computed': indicator.computed}
      columns.push(indicator.id)
    })
    this.table.data = this._getPickValue(items, locations)
    this.table.schema = this._buildSchema(parseSchema(datapoints), fields)
    this.table.fields = fields
    this.table.columns = columns
    this.trigger(this.table)
  }
})

export default DataBrowserTableStore
