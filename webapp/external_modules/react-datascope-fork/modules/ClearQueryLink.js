import React from 'react/addons'
import InterfaceMixin from '../InterfaceMixin'

// Datascope module which clears existing filters, searches and sorts, and resets to first page
// (each type can be selectively disabled with clearWhatever = false)
// renders children wrapped in a clickable div

let ClearQueryLink = React.createClass({
  displayName: 'ClearQueryLink',

  mixins: [(0, InterfaceMixin)('Datascope')],

  propTypes: {
    children: React.PropTypes.array,
    onChangeQuery: React.PropTypes.func,
    clearFilters: React.PropTypes.bool,
    clearSearch: React.PropTypes.bool,
    clearSort: React.PropTypes.bool,
    clearPagination: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      clearFilters: true,
      clearSearch: true,
      clearSort: true,
      clearPagination: true
    }
  },

  onClick: function () {
    let _props = this.props
    let clearFilters = _props.clearFilters
    let clearSearch = _props.clearSearch
    let clearSort = _props.clearSort
    let clearPagination = _props.clearPagination

    let query = this.props.query

    if (clearFilters) query = React.addons.update(query, { filter: { $set: undefined } })
    if (clearSearch) query = React.addons.update(query, { search: { $set: undefined } })
    if (clearSort) query = React.addons.update(query, { sort: { $set: undefined } })
    if (clearPagination && query.pagination) query = React.addons.update(query, { pagination: { $merge: { page: 1, offset: 0 } } })
    this.props.onChangeQuery(query)
  },

  render: function () {
    let content = this.props.children || 'Clear filters'

    return React.createElement(
      'div',
      { className: 'ds-clear-query-link', onClick: this.onClick },
      content
      )
  }
})

export default ClearQueryLink
