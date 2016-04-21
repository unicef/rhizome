import _ from 'lodash'
import React from 'react'

let TableHeaderCell = React.createClass({
  propTypes: {
    schema: React.PropTypes.shape({
      name: React.PropTypes.string,
      title: React.PropTypes.string
    }), // schema for this field
    field: React.PropTypes.object,
    title: React.PropTypes.string, // to override schema title
    onClick: React.PropTypes.func, // usually the sort function
    isSortedBy: React.PropTypes.bool, // true if the table is sorted by this column
    sortIndicatorAscending: React.PropTypes.string,
    sortIndicatorDescending: React.PropTypes.string,
    sortOrder: React.PropTypes.string
  },

  getDefaultProps: function getDefaultProps () {
    return {
      onClick: null,
      sortIndicatorAscending: ' ▲',
      sortIndicatorDescending: ' ▼'
    }
  },

  _getTitle: function _getTitle () {
    return _.isUndefined(this.props.title) ? this.props.field.title : this.props.title
  },

  render: function render () { console.info('TableHeaderCell - render')
    const props = this.props
    let isSortAscending = (props.sortOrder || '').toLowerCase().indexOf('asc') === 0
    let sortIndicator = props.isSortedBy ? isSortAscending ? props.sortIndicatorAscending : props.sortIndicatorDescending : ''
    return (
      <th className='ds-data-table-col-head' onClick={props.onClick}>
        <span className='ds-data-table-col-title'>{props.name !== 'location' ? this._getTitle() : ''}</span>
        <span className='ds-data-table-sort-indicator'>{sortIndicator}</span>
      </th>
    )
  }
})

export default TableHeaderCell