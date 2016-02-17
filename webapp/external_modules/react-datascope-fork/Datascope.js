import _ from 'lodash'
import React from 'react/addons'
import numeral from 'numeral'
import moment from 'moment'

/**
 * Datascope is the main wrapper class which passes data down the tree (to children as props.data)
 * and queries back up the tree (via the onChangeQuery callback).
 */

let Datascope = React.createClass({
  displayName: 'Datascope',

  propTypes: {
    data: React.PropTypes.array, // the (filtered/searched/sorted/paginated) data to display
    children: React.PropTypes.array,
    schema: React.PropTypes.shape({ // json-schema representing the shape of the data
      items: React.PropTypes.shape({
        properties: React.PropTypes.object
      })
    }),
    query: React.PropTypes.shape({
      search: React.PropTypes.objectOf(React.PropTypes.shape({
        value: React.PropTypes.string,
        fields: React.PropTypes.array
      })),
      sort: React.PropTypes.shape({
        key: React.PropTypes.string,
        order: React.PropTypes.string
      }),
      filter: React.PropTypes.objectOf(React.PropTypes.object)
    }),
    onChangeQuery: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      query: {},
      onChangeQuery: function () {}
    }
  },

  componentWillMount: function () {
    // generate fields from schema properties, but override them with any passed in this.props.fields
    // let fields = _.assign({}, fieldsFromSchema(this.props.schema), this.props.fields)

    let _initFields = initFields(this.props.fields, this.props.schema)

    let fields = _initFields.fields
    let orderedFields = _initFields.orderedFields

    this.setState({ fields: fields, orderedFields: orderedFields })
  },

  onChangeSearch: function (searchId, value, fields) {
    let query = null
    if (!_.isObject(this.props.query.search)) {
      query = React.addons.update(this.props.query, { search: { $set: _defineProperty({}, searchId, { value: value, fields: fields }) } })
    } else {
      query = React.addons.update(this.props.query, { search: _defineProperty({}, searchId, { $set: { value: value, fields: fields } }) })
    }

    this.props.onChangeQuery(query)
  },

  onChangeSort: function (key, order) {
    order = order || 'descending'
    let sortObj = _.isUndefined(key) || _.isNull(key) ? undefined : { key: key, order: order }
    let query = React.addons.update(this.props.query, { sort: { $set: sortObj } })

    this.props.onChangeQuery(query)
  },

  onChangeFilter: function (key, filterObj) {
    let query = null
    if (!_.isObject(this.props.query.filter)) {
      query = React.addons.update(this.props.query, { filter: { $set: _defineProperty({}, key, filterObj) } })
    } else {
      query = React.addons.update(this.props.query, { filter: { $merge: _defineProperty({}, key, filterObj) } })
    }

    this.props.onChangeQuery(query)
  },

  onChangePagination: function (pagination) {
    // todo keep all the pagination things in sync - let paginator just change page and auto update the rest
    let query = React.addons.update(this.props.query, { pagination: { $set: pagination } })
    this.props.onChangeQuery(query)
  },

  render: function () {
    let query = this.props.query
    let onChangeSearch = this.onChangeSearch
    let onChangeSort = this.onChangeSort
    let onChangeFilter = this.onChangeFilter
    let onChangePagination = this.onChangePagination
    let _state = this.state
    let fields = _state.fields
    let orderedFields = _state.orderedFields
    let datascopeProps = _.assign({}, _.pick(this.props, ['data', 'schema', 'query', 'onChangeQuery']), { fields: fields, orderedFields: orderedFields })
    let filterProps = { onChangeFilter: onChangeFilter, filter: _.isObject(query.filter) ? query.filter : {} }
    let searchProps = { onChangeSearch: onChangeSearch }
    let sortProps = { onChangeSort: onChangeSort,
      sort: _.isObject(query.sort) ? query.sort : {},
      sortKey: query.sort ? query.sort.key : null,
      sortOrder: query.sort ? query.sort.order : null
    }

    let paginationProps = {
      onChangePagination: onChangePagination,
      pagination: _.isObject(query.pagination) ? query.pagination : {}
    }

    // Recursively traverse children, cloning Datascope modules and adding their required props
    // React 0.14 should introduce a new feature: parent-based contexts
    // When 0.14 lands, we may be able to use context for this instead
    return React.createElement(
      'div',
      null,
      this.recursiveCloneChildren(this.props.children, datascopeProps, sortProps, filterProps, searchProps, paginationProps)
      )
  },

  recursiveCloneChildren: function (children, datascopeProps, sortProps, filterProps, searchProps, paginationProps) {
    let _this = this

    return React.Children.map(children, function (child) {
      if (!_.isObject(child)) return child

      let childImplements = _.isFunction(child.type.implementsInterface) ? child.type.implementsInterface : function () {
        return false
      }

      let childProps = {}

      if (childImplements('Datascope')) {
        if (childImplements('DatascopeSearch')) {
          let searchQuery = _.isObject(datascopeProps.query.search) ? datascopeProps.query.search[child.props.id] : undefined
          let searchValue = _.isObject(searchQuery) ? searchQuery.value || '' : ''
          searchProps = _.assign({}, searchProps, {
            value: searchValue
          })
        }

        childProps = _.extend(childProps, datascopeProps, childImplements('DatascopeSort') ? sortProps : null, childImplements('DatascopeFilter') ? filterProps : null, childImplements('DatascopeSearch') ? searchProps : null, childImplements('DatascopePagination') ? paginationProps : null)
      }

      childProps.children = _this.recursiveCloneChildren(child.props.children, datascopeProps, sortProps, filterProps, searchProps)

      return React.cloneElement(child, childProps)
    })
  }
})

let fieldDefaults = {
  numberFormat: '0,0',
  dateFormat: '',
  test: 'd',
  renderers: {
    string: _.identity,
    boolean: function (v) {
      return v + ''
    },
    number: function (v) {
      return v + ''
    },
    'null': function (v) {
      return v + ''
    },
    array: function (v) {
      return v && v.length ? v.join(', ') : v + ''
    },
    oneOf: function (v, field, _ref) {
      let moment = _ref.moment
      let numeral = _ref.numeral

      let valueSchema = _.find(field.schema.oneOf, function (s) {
        return s['enum'][0] === v
      })
      return valueSchema ? valueSchema.title || v + '' : v + ''
    }
  }
}

function initFields (definedFields, schema) {
  let fields = fieldsFromSchema(schema)

  _.each(definedFields, function (definedField, fieldName) {
    // either fieldName must be in fields, or field must have .key attribute
    let fieldKey = _.has(definedField, 'key') ? definedField.key : fieldName in schema.items.properties ? fieldName : null
    if (!fieldKey) throw 'Datascope: could not match field ' + fieldName + 'to a schema property'
    // fill in unknown (implicit) parts of defined fields
    let fieldSchema = schema.items.properties[fieldKey]
    let fieldProps = _.pick(definedField, ['title', 'weight', 'renderer', 'format'])
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
    if (fieldName in fields) {
      _.assign(fields[fieldName], fieldProps)
    } else {
      fields[fieldName] = fieldProps
    }
  })

  let orderedFields = _.sortBy(fields, 'weight')

  return { fields: fields, orderedFields: orderedFields }
}

function fieldsFromSchema (schema) {
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
}

function _defineProperty (obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true })
  } else {
    obj[key] = value
  } return obj
}

export default Datascope
