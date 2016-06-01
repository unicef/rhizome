import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import React from 'react'
import Reflux from 'reflux'
import parseSchema from 'components/organisms/manage-system/utils/parseSchema'
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

  getRowData: function () {
    const rows = []
    const grouped_by_location = _.groupBy(this.props.data, 'location.id')
    _.map(grouped_by_location, datapoint_group => {
      const first_datapoint = datapoint_group[0]
      const row = {
        campaign: moment(first_datapoint.campaign.start_date).format('MMM YYYY'),
        campaign_id: first_datapoint.campaign.id,
        location: first_datapoint.location.name,
        location_id: first_datapoint.location.id
      }
      datapoint_group.forEach(datapoint => row[datapoint.indicator.id] = {
        value: this._format(datapoint.value),
        computed: datapoint.id
      })
      rows.push(row)
    })
    return rows
  },

  render: function () {
    const props = this.props
    if (!props.data || props.data.length === 0) {
      return <div className='medium-12 columns ds-data-table-empty'>No data.</div>
    } else {
      let fields = {location: {title: 'Location', name: 'location'}}
      let columns = ['location']
      if (!props.hideCampaigns) {
        fields.campaign = {title: 'Campaign', name: 'campaign'}
        columns.push('campaign')
      }
      props.selected_indicators.forEach(indicator => {
        fields[indicator.id] = {title: indicator.short_name, name: indicator.id, 'computed': indicator.computed, 'source_name': indicator.source_name, 'data_format': indicator.data_format}
        columns.push(indicator.id)
      })

      const data = this.getRowData()
      const schema = parseSchema(props.data)
      schema.items.properties = fields

      return (
        <LocalDatascope data={data} schema={schema} pageSize={10}>
          <Datascope>
            <SimpleDataTable editable={props.editable} rowAction={props.rowAction}>
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
