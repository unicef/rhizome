import _ from 'lodash'
import moment from 'moment'
import React from 'react'
import Table from 'components/table/Table'
import DatapointTableCell from 'components/table/DatapointTableCell'

class DatapointTable extends Table {

  constructor (props) {
    super(props)
    this.groupByIndicator = this.props.groupBy === 'indicator'
    this.groupByCampaign = this.props.groupByTime === 'campaign'
    this.rows = this.groupByIndicator ? _.groupBy(this.props.datapoints.flattened, 'indicator.id') : this.props.datapoints.grouped
  }

  onSave = function () {
    console.log('On Save')
  }

  renderHeaderRow = function () {
    const first_row = _.toArray(this.rows)[0]
    const header_cells = first_row.map(datapoint => {
      const entity = this.groupByCampaign ? datapoint.campaign : datapoint.indicator
      return <th>{entity.short_name || entity.name}</th>
    })
    return (
      <tr>
        <th></th>
        { !this.groupByIndicator ? <th>{_.capitalize(this.props.groupByTime)}</th> : null}
        { header_cells }
      </tr>
    )
  }

  renderRows = function () {
    const groupByYear = this.props.groupByTime === 'year'
    const rows = groupByYear ? _.toArray(this.rows).reverse() : this.rows
    return _.map(rows, (row, key) => {
      const first_cell = row[0]
      const entity = this.groupByIndicator ? first_cell.indicator : first_cell.location
      const indicator = this.props.indicators_index[key]
      const date_format = groupByYear ? 'YYYY' : 'MMM YYYY'
      const date = groupByYear ? first_cell.time_grouping : moment(first_cell.campaign.start_date).format(date_format)
      return (
        <tr>
          <td><strong>{entity.name}</strong></td>
          { !this.groupByIndicator ? <td>{date}</td> : null}
          { _.map(row, datapoint => <DatapointTableCell datapoint={datapoint} onSave={this.props.editable ? this.onSave : null} />) }
        </tr>
      )
    })
  }

  _getFormattedValue = function (indicator) {
    if (indicator.data_format === 'pct') {}
    const value = indicator.value
    return value
  }
}

export default DatapointTable
