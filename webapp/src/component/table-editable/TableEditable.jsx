import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import d3 from 'd3'

import Cell from 'component/table-editable/Cell.jsx'
import TableEditableStore from 'stores/TableEditableStore'
import TableEditableActions from 'actions/TableEditableActions'

let TableEditable = React.createClass({
  mixins: [Reflux.connect(TableEditableStore)],

  propTypes: {
    data: React.PropTypes.array,
    loaded: React.PropTypes.bool,
    indicatorSet: React.PropTypes.object,
    indicatorMap: React.PropTypes.object,
    locationMap: React.PropTypes.object,
    locations: React.PropTypes.array,
    campaignId: React.PropTypes.string
  },

  componentWillReceiveProps: function (nextProps) {
    if (!this.props.loaded && nextProps.loaded) {
      TableEditableActions.init(nextProps.data, nextProps.indicatorSet,
        nextProps.indicatorMap, nextProps.locationMap,
        nextProps.locations, nextProps.campaignId)
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return !_.isEqual(nextProps.loaded, this.props.loaded) || !_.isEqual(this.state.processed, nextState.processed)
  },

  completionClass: function (v) {
    if (v === 0) {
      return 'statusText-bad'
    } else if (v === 1) {
      return 'statusText-good'
    } else if (v > 0 && v < 1) {
      return 'statusText-okay'
    }
    return null
  },

  percent: function (v) {
    const percent = d3.format('%')
    return percent(v)
  },

  _buildTable: function () {
    let contentTitle = (
      <div>
        <h5>
          Form is <span className={this.completionClass(this.state.total.complete / this.state.total.total)}>
          {this.percent(this.state.total.complete / this.state.total.total)} </span>
           complete ({this.state.total.complete} / {this.state.total.total} values entered)
        </h5>
      </div>
    )

    let tableHeader = ''
    let tableBody = ''

    if (this.state.table.rows.length > 0) {
      tableHeader = this.state.table.columns.map(column => {
        return (
          <tr>
            <th></th>
            <th className={column.headerClasses}>
              <div className='th-inner'>
                {column.header}
                <div className='completionStatus'>
                  {this.state.total.complete} / {this.state.total.total}
                </div>
              </div>
            </th>
          </tr>
        )
      })
    }

    tableBody = this.state.table.rows.map(row => {
      return (
        <tr>
          <td className='rowCompletionStatus'>
            <div className='completionStatus'>
              {this.state.total.complete} / {this.state.total.total}
            </div>
          </td>
          <td>
            <Cell />
          </td>
        </tr>
      )
    })

    let tableContent = (
      <div>
        {contentTitle}
        <div className='fixed-table-container'>
          <div className='header-background'></div>
          <div className='fixed-table-container-inner'>
            <table>
              <thead>
                {tableHeader}
              </thead>
              <tbody>
                {tableBody}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    )

    return tableContent
  },

  render: function () {
    if (!this.props.loaded || !this.state.processed) {
      return (<div className='empty'>Use the options above to load a data entry form.</div>)
    } else if (this.props.indicatorSet.indicators.length < 1) {
      return (<div className='empty'>Use the options above to load a data entry form.</div>)
    } else {
      return this._buildTable()
    }
  }
})

export default TableEditable
