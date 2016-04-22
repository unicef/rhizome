import _ from 'lodash'
import React from 'react'
import Table from 'components/molecules/tables/Table'
import DatapointTableCell from 'components/molecules/tables/DatapointTableCell'

class DatapointTable extends Table {

  constructor (props) {
    super(props)
    this.groupByIndicator = this.props.groupBy === 'indicator'
    this.rows = this.groupByIndicator ? _.groupBy(this.props.datapoints.flattened, 'indicator') : this.props.datapoints.raw
  }

  onSave = function () {
    console.log('On Save')
  }

  renderHeaderRow = function () {
    const first_row = this.groupByIndicator ? _.toArray(this.rows)[0] : _.toArray(this.rows)[0].indicators
    const header_cells = first_row.map(datapoint => {
      const entity = this.groupByIndicator ? datapoint.campaign : this.props.indicators_index[datapoint.indicator]
      return <th>{entity.name}</th>
    })
    return (
      <tr>
        <th></th>
        { !this.groupByIndicator ? <th>Campaign</th> : null}
        { header_cells }
      </tr>
    )
  }

  renderRows = function () {
    return _.map(this.rows, (row, key) => {
      const indicator = this.props.indicators_index[key]
      const entity = this.groupByIndicator ? indicator : this.props.locations_index[row.location]
      return (
        <tr>
          <td><strong>{entity.name}</strong></td>
          { !this.groupByIndicator ? <td>{row.campaign.name}</td> : null}
          { this.renderCells(row, indicator) }
        </tr>
      )
    })
  }

  renderCells = function (row, indicator) {
    const saveHandler = this.props.editable ? this.onSave : null
    const cells = this.groupByIndicator ? row : row.indicators
    return _.map(cells, datapoint => {
      indicator = this.groupByIndicator ? indicator : this.props.indicators_index[datapoint.indicator]
      return <DatapointTableCell indicator={indicator} datapoint={datapoint} onSave={saveHandler} />
    })
  }

  _getFormattedValue = function (indicator) {
    if (indicator.data_format === 'pct') {}
    const value = indicator.value
    return value
  }
}

export default DatapointTable
