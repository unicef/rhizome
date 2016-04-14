import _ from 'lodash'
import React from 'react'
import moment from 'moment'
import numeral from 'numeral'

var PropTypes = React.PropTypes

/**
 * Datascope is the main wrapper class which passes data down the tree (to children as props.data)
 * and queries back up the tree (via the onChangeQuery callback).
 */

var Datascope = React.createClass({
  displayName: 'Datascope',

  propTypes: {
    data: PropTypes.array, // the (filtered/searched/sorted/paginated) data to display
    schema: PropTypes.shape({ // json-schema representing the shape of the data
      items: PropTypes.shape({
        properties: PropTypes.object
      })
    }),
    query: PropTypes.shape({
      search: PropTypes.objectOf(PropTypes.shape({
        value: PropTypes.string,
        fields: PropTypes.array
      })),
      sort: PropTypes.shape({
        key: PropTypes.string,
        order: PropTypes.string
      }),
      filter: PropTypes.objectOf(PropTypes.object)
    }),
    onChangeQuery: React.PropTypes.func
  },

  _defineProperty (obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true })
    // React.addons.update(this.props.query, { search: { $set: _defineProperty({}, searchId, { value: value, fields: fields }) } })
    } else {
      obj[key] = value
    }
    return obj
  },

  initFields (definedFields, schema) {
    var fields = this.fieldsFromSchema(schema)

    _.each(definedFields, function (definedField, fieldName) {
      // either fieldName must be in fields, or field must have .key attribute
      var fieldKey = _.has(definedField, 'key') ? definedField.key : fieldName in schema.items.properties ? fieldName : null
      if (!fieldKey) throw 'Datascope: could not match field ' + fieldName + 'to a schema property'
      // fill in unknown (implicit) parts of defined fields
      var fieldSchema = schema.items.properties[fieldKey]
      var fieldProps = _.pick(definedField, ['title', 'weight', 'renderer', 'format', 'source_name', 'data_format'])
      fieldProps.name = fieldName
      fieldProps.key = fieldKey
      if (fieldProps.format && !fieldProps.renderer) {
        if (fieldSchema.type === 'number' || fieldSchema.type === 'integer') {
          fieldProps.renderer = function (v, field) {
            return numeral(v).format(fieldProps.format)
          }
        } else if (fieldSchema.type === 'string' && fieldSchema.format === 'date-time') {
          fieldProps.renderer = function (v, field) {
            return moment(v).format(fieldProps.format)
          }
        }
      }
      // override the default field props (from schema) with user-provided field props
      if (fieldName in fields) _.assign(fields[fieldName], fieldProps);else fields[fieldName] = fieldProps
    })

    var orderedFields = _.sortBy(fields, 'weight')

    return { fields: fields, orderedFields: orderedFields }
  },

  fieldsFromSchema (schema) {
    var fieldDefaults = {
      numberFormat: '0,0',
      dateFormat: '',
      test: 'd',
      renderers: {
        string: _.identity,
        boolean: function defaultBooleanRenderer (v) {
          return v + ''
        },
        number: function defaultNumberRenderer (v) {
          return v + ''
        },
        'null': function defaultNullRenderer (v) {
          return v + ''
        },
        array: function defaultArrayRenderer (v) {
          return v && v.length ? v.join(', ') : v + ''
        },
        oneOf: function defaultOneOfRenderer (v, field, _ref) {
          // var moment = _ref.moment
          // var numeral = _ref.numeral

          var valueSchema = _.find(field.schema.oneOf, function (s) {
            return s['enum'][0] === v
          })
          return valueSchema ? valueSchema.title || v + '' : v + ''
        }
      }
    }

    if (!schema || !schema.items || !schema.items.properties) return []

    return _(schema.items.properties).map(function (propSchema, key) {
      return [key, {
        title: propSchema.title || key,
        key: key,
        name: key,
        schema: propSchema,
        renderer: propSchema.oneOf && _.every(propSchema.oneOf, function (s) {
          return s.title && s['enum'] && s['enum'].length === 1
        }) ? fieldDefaults.renderers.oneOf : propSchema.type && propSchema.type in fieldDefaults.renderers ? fieldDefaults.renderers[propSchema.type] : function (v) {
          return v + ''
        }
      }]
    }).object().value()
  },

  getDefaultProps () {
    return {
      query: {},
      onChangeQuery: function onChangeQuery () {}
    }
  },

  componentWillMount () {
    // generate fields from schema properties, but override them with any passed in this.props.fields
    // var fields = _.assign({}, fieldsFromSchema(this.props.schema), this.props.fields)

    var _initFields = this.initFields(this.props.fields, this.props.schema)

    var fields = _initFields.fields
    var orderedFields = _initFields.orderedFields

    this.setState({ fields: fields, orderedFields: orderedFields })
  },

  onChangeSearch(searchId, value, fields) {
    var query = this.props.query
    query.search = this._defineProperty({}, searchId, { value: value, fields: fields })

    this.props.onChangeQuery(query)
  },

  onChangeSort(key, order) {
    order = order || 'descending'
    var sortObj = _.isUndefined(key) || _.isNull(key) ? undefined : { key: key, order: order }
    var query = this.props.query
    query.sort = sortObj
    this.props.onChangeQuery(query)
  },

  onChangeFilter(key, filterObj) {
    // used in FilterPanel component but not being used anywhere. waiting for refactor or omition?
    // check with Ersan if broken
    var query = this.props.query
    if (!_.isObject(this.props.query.filter)) {
      query.filter = filterObj
    } else {
      _.merge(query.filter, filterObj)
    }
    this.props.onChangeQuery(query)
  },

  onChangePagination(pagination) {
    // todo keep all the pagination things in sync - let paginator just change page and auto update the rest
    var query = this.props.query
    query.pagination = pagination
    this.props.onChangeQuery(query)
  },

  render() {
    var query = this.props.query
    var onChangeSearch = this.onChangeSearch
    var onChangeSort = this.onChangeSort
    var onChangeFilter = this.onChangeFilter
    var onChangePagination = this.onChangePagination
    var _state = this.state
    var fields = _state.fields
    var orderedFields = _state.orderedFields

    var datascopeProps = _.assign({}, _.pick(this.props, ['data', 'schema', 'query', 'onChangeQuery']), { fields: fields, orderedFields: orderedFields })
    var sortProps = { onChangeSort: onChangeSort,
      sort: _.isObject(query.sort) ? query.sort : {},
      sortKey: query.sort ? query.sort.key : null,
      sortOrder: query.sort ? query.sort.order : null
    }
    var filterProps = { onChangeFilter: onChangeFilter, filter: _.isObject(query.filter) ? query.filter : {} }
    var searchProps = { onChangeSearch: onChangeSearch }

    var paginationProps = {
      onChangePagination: onChangePagination,
      pagination: _.isObject(query.pagination) ? query.pagination : {}
    }

    // Recursively traverse children, cloning Datascope modules and adding their required props
    // React 0.14 should introduce a new feature: parent-based contexts
    // When 0.14 lands, we may be able to use context for this instead
    return (
    <div>
      {this.recursiveCloneChildren(this.props.children, datascopeProps, sortProps, filterProps, searchProps, paginationProps)}
    </div>
    )
  },
  recursiveCloneChildren(children, datascopeProps, sortProps, filterProps, searchProps, paginationProps) {
    var self = this
    return React.Children.map(children, function (child) {
      if (!_.isObject(child)) return child

      var childImplements = _.isFunction(child.type.implementsInterface) ? child.type.implementsInterface : function () {
        return false
      }
      var childProps = {}

      if (childImplements('Datascope')) {
        if (childImplements('DatascopeSearch')) {
          var searchQuery = _.isObject(datascopeProps.query.search) ? datascopeProps.query.search[child.props.id] : undefined
          var searchValue = _.isObject(searchQuery) ? searchQuery.value || '' : ''
          searchProps = _.assign({}, searchProps, {
            value: searchValue
          })
        }

        childProps = _.extend(childProps, datascopeProps, childImplements('DatascopeSort') ? sortProps : null, childImplements('DatascopeFilter') ? filterProps : null, childImplements('DatascopeSearch') ? searchProps : null, childImplements('DatascopePagination') ? paginationProps : null)
      }

      childProps.children = self.recursiveCloneChildren(child.props.children, datascopeProps, sortProps, filterProps, searchProps)

      return React.cloneElement(child, childProps)
    })
  }
})

export default Datascope

// datascope will keep a query object in state which represents all the rules by which the data will be displayed:
// `fields` limits which data fields are used
// `filters` are simple filters for individual column values, allowed filter types:
//      `eq` - exact match
//      `lt` - less than (number only)
//      `gt` - greater than (number only)
//      `in` - list of values, of which the column value must be one
//      `intersects` - for data type `array` only, a list of values which filter the data such that:
//                     length(intersection(dataList, thisList)) > 0
// `searches` are search terms meant to fuzzy match, potentially against multiple fields
// `sort` describes how the data should be sorted (column key and order)

// var mockQuery = {
//    fields: ['name', 'age', 'company', 'gender', 'email'],
//    filters: {
//        isActive: { eq: true },
//        age: { gt: 30 }
//    },
//    search: {
//        search1: {
//            value: 'com', // the string to search for
//            fields: ['email', 'name']
//        }
//    },
//    sort: {
//        key: 'age',
//        order: 'descending'
//    }
// }
