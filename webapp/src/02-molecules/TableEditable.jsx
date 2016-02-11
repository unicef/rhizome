import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import d3 from 'd3'

import Cell from '02-molecules/TableEditableCell.jsx'
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
    return !_.isEqual(nextProps.loaded, this.props.loaded) ||
      !_.isEqual(this.state.processed, nextState.processed) ||
      nextState.total !== this.state.total
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
      tableHeader = this.state.table.columns.map((column, index) => {
        let isShowLabel = column.type !== 'value'
        let className = (isShowLabel ? 'col' : this.completionClass(this.state.byColumn[index].complete / this.state.byColumn[index].total)) + ' completionStatus'
        let headerContent = isShowLabel ? '' : this.state.byColumn[index].complete + ' / ' + this.state.byColumn[index].total
        return (
          <th className={column.headerClasses}>
            <div className='th-inner'>
              {column.header}
              <div className={className}>
                {headerContent}
              </div>
            </div>
          </th>
        )
      })
    }

    tableBody = this.state.table.rows.map((row, index) => {
      let className = this.completionClass(this.state.byRow[index].complete / this.state.byRow[index].total) + ' completionStatus'
      let cellItems = row.map(item => <Cell item={item} />)
      return (
        <tr>
          <td className='rowCompletionStatus entry-table-row-header'>
            <div className={className}>
              {this.state.byRow[index].complete} / {this.state.byRow[index].total}
            </div>
          </td>
          {cellItems}
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
                <tr>
                  <th></th>
                  {tableHeader}
                </tr>
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
