import _ from 'lodash'
import React from 'react'
import moment from 'moment'

var LocalDatascope = React.createClass({
  displayName: 'LocalDatascope',

  propTypes: {
    data: React.PropTypes.array,
    schema: React.PropTypes.object,
    initialQuery: React.PropTypes.object,
    pageSize: React.PropTypes.number,
    paginated: React.PropTypes.bool,
    children: React.PropTypes.array
  },

  stringComparator (a, b) {
    var aLower = (a + '').toLowerCase()
    var bLower = (b + '').toLowerCase()
    return aLower > bLower ? 1 : aLower < bLower ? -1 : 0
  },
  numberComparator (a, b) {
    return a > b ? 1 : a < b ? -1 : 0
  },

  matchesFilter (objToTest, filter, key) {
    // matcher for our filter query language
    if (!filter) return true
    var value = objToTest[key]
    if ('eq' in filter) return value === filter.eq
    if (_.isArray(filter['in'])) return filter['in'].indexOf(value) >= 0
    if (_.isArray(filter.intersects)) {
      return _.intersection(filter.intersects, _.pluck(value, 'value')).length > 0
    }
    if (_.isNumber(filter.gt) || _.isNumber(filter.lt)) {
      return ('gt' in filter ? value >= filter.gt : true) && ('lt' in filter ? value <= filter.lt : true)
    } else if (_.isDate(filter.gt) || _.isDate(filter.lt)) {
      return ('gt' in filter ? moment(value) >= filter.gt : true) && ('lt' in filter ? moment(value) <= filter.lt : true)
    }
    return true
  },

  getDefaultProps () {
    return {
      paginated: true,
      pageSize: 200
    }
  },
  getInitialState () {
    return {
      displayData: _.clone(this.props.data),
      query: this.props.initialQuery || {}
    }
  },

  componentWillMount () {
    var query = this.state.query
    if (this.props.paginated) {
        query.pagination = { page: 1,
                             offset: 0,
                             limit: this.props.pageSize,
                             total: this.props.data.length
                           }
    }
    this.setState(this._getDisplayData(query))
  },

  componentWillReceiveProps (nextProps) {
    this.props = nextProps
    this.setState(this._getDisplayData(this.state.query))
  },

  _getDisplayData (query) {

    var hasFilter = _.isObject(query.filter) && _.keys(query.filter).length
    var hasSearch = _.isObject(query.search) && _.keys(query.search).length
    var hasSort = query.sort && !_.isUndefined(query.sort.key)
    var hasPagination = _.isObject(query.pagination)

    var displayData = _.clone(this.props.data)

    displayData = hasFilter ? this._filterData(displayData, query.filter) : displayData
    displayData = hasSearch ? this._searchData(displayData, query.search) : displayData
    displayData = hasSort ? this._sortData(displayData, query.sort) : displayData
    if (hasPagination) {
      var paginated = this._paginateData(displayData, query)
      displayData = paginated.data
      query = _.assign({}, query, { pagination: paginated.pagination })
    }
    return { query: query, displayData: displayData }
  },

  _filterData (data, filterQuery) {
    return _.filter(data, function (d) {
      return _.all(filterQuery, function (filterObj, key) {
        return this.matchesFilter(d, filterObj, key)
      })
    })
  },
  _searchData (data, searchQueries) {
    var propSchemas = this.props.schema.items.properties
    var stringyFieldKeys = _(propSchemas).keys().filter(function (key) {
      return _.includes(['string', 'number'], propSchemas[key].type)
    }).value()
    return _.filter(data, function (d) {
      return _.any(searchQueries, function (searchQuery) {
        var searchableKeys = searchQuery.fields || stringyFieldKeys
        return _.any(searchableKeys, function (key) {
          return (d[key] + '').toLowerCase().indexOf(searchQuery.value.toLowerCase()) > -1
        })
      })
    })
  },
  _sortData (data, sortQuery) {
    var self = this
    // WARNING this mutates the data array so call it with a copy
    // return _.sortBy(data, sortQuery.key)
    return data.sort(function (a, b) {
      var key = sortQuery.key
      var order = sortQuery.order.toLowerCase().indexOf('asc') === 0 ? -1 : 1
      var field = self.props.schema.items.properties[key]
      var comparator = field.type === 'string' ? self.stringComparator : self.numberComparator
      return comparator(a[key], b[key]) * order
    })
  },
  _paginateData (data, query) {
    var pagination = query.pagination

    var prevQuery = this.state.query

    // if filter/search/sort changed, or pagination is past the end of data, reset to page 1 of results
    var hasChanged = _.any(['filter', 'search', 'sort'], function (key) {
      return prevQuery[key] !== query[key]
    })
    var isPastEnd = pagination.offset >= data.length
    pagination = hasChanged || isPastEnd ? { page: 1, offset: 0, limit: pagination.limit, total: data.length } : _.assign({}, pagination, { total: data.length })

    // trim the data to paginate from [offset] to [offset + limit]
    var pageEndIndex = Math.min(pagination.offset + pagination.limit - 1, data.length - 1)
    data = data.slice(pagination.offset, pageEndIndex + 1)

    return { data: data, pagination: pagination }
  },

  onChangeQuery (query) {
    var newState = this._getDisplayData(query)
    this.setState(newState)
  },

  render () {
    var self = this
    //this MUST be refactored.
    return React.createElement(
      'div',
      { className: 'local-datascope' },
      React.Children.map(this.props.children, function (child) {
        return React.cloneElement(child, _.assign({}, _.omit(self.props, ['children']), {
          onChangeQuery: self.onChangeQuery,
          data: self.state.displayData,
          query: self.state.query
        }))
      })
    )
  }
})

export default LocalDatascope
