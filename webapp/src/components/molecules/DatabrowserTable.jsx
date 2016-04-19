import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import React from 'react'
import Reflux from 'reflux'
import parseSchema from 'components/organisms/manage-system/utils/parseSchema'
import DataBrowserTableStore from 'stores/DataBrowserTableStore'
import DataBrowserTableActions from 'actions/DataBrowserTableActions'
import SimpleDataTable from 'components/organisms/datascope/SimpleDataTable'

import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import Paginator from 'components/organisms/datascope/Paginator'
import LocalDatascope from 'components/organisms/datascope/LocalDatascope'
import Datascope from 'components/organisms/datascope/Datascope'

let DatabrowserTable = React.createClass({

  propTypes: {
    data: React.PropTypes.object,
    editable: React.PropTypes.bool,
    selected_locations: React.PropTypes.array.isRequired,
    selected_indicators: React.PropTypes.array.isRequired,
    hideCampaigns: React.PropTypes.bool
  },

  getDefaultProps() {
    return {
      hideCampaigns: false
    }
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

  _extractItemsFromData: function (datapoints) {
    return datapoints.map(item => {
      let result = _.pick(item, 'location')
      result.campaign = moment(item.campaign.start_date).format('MMM YYYY')
      result.location_id = item.location
      result.campaign_id = item.campaign
      item.indicators.forEach(indicator => {
        result[indicator.indicator] = { // indicator.indicator is the id
          value: this._format(indicator.value),
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

  render: function () {
    if (!this.props.data) {
      return <div className='medium-12 columns ds-data-table-empty'>No data.</div>
    } else {
      let fields = {location: {title: 'Location', name: 'location'}, campaign: {title: 'Campaign', name: 'campaign'}}
      let columns = ['location', 'campaign']
      this.props.selected_indicators.forEach(indicator => {
        fields[indicator.id] = {title: indicator.name, name: indicator.id, 'computed': indicator.computed, 'source_name': indicator.source_name, 'data_format': indicator.data_format}
        columns.push(indicator.id)
      })
      const items = this._extractItemsFromData(this.props.data || [])
      const data = this._getPickValue(items, this.props.selected_locations)
      const schema = parseSchema(this.props.data)
      schema.items.properties = fields

      return (
        <LocalDatascope data={data} schema={schema} pageSize={10}>
          <Datascope>
            <SimpleDataTable editable={this.props.editable}>
              { columns.map(column => <SimpleDataTableColumn name={column}/>) }
            </SimpleDataTable>
            <Paginator />
          </Datascope>
        </LocalDatascope>
      )
    }
  }
})

export default DatabrowserTable
