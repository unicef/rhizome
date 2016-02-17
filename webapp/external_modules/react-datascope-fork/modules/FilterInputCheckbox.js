import _ from 'lodash'
import React from 'react/addons'

let FilterInputCheckbox = React.createClass({
  displayName: 'FilterInputCheckbox',

  propTypes: {
    // schema describing the field
    schema: React.PropTypes.shape({
      name: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
      title: React.PropTypes.string,
      type: React.PropTypes.string,
      constraints: React.PropTypes.shape({
        oneOf: React.PropTypes.array,
        items: React.PropTypes.shape({
          oneOf: React.PropTypes.array
        })
      })
    }),
    filter: React.PropTypes.object,

    // provide name, label, values to override the schema
    // unique name for this collection of checkboxes (for name attribute)
    name: React.PropTypes.string,
    // human-readable label for this collection of checkboxes
    label: React.PropTypes.string,
    // list of possible values for the checkboxes, in one of two formats:
    // ['val1', 'val2', 'val3', ...] // OR...
    // [{label: "Value 1", value: 'val1'}, {label: "Value 2", value: 'val2'}, ...]
    // if the former, array values will be used for both labels and input values
    values: React.PropTypes.array
  },
  componentWillMount: function () {
    this._validateProps()
  },
  componentWillReceiveProps: function () {
    this._validateProps()
  },

  _validateProps: function () {
    if (_.isNull(this._getName())) throw 'FilterInputCheckbox requires schema or `name` prop'
      if (_.isNull(this._getValues())) throw 'FilterInputCheckbox requires schema or `values` prop'
    },
  _getName: function () {
    return _.isString(this.props.name) ? this.props.name : _.isObject(this.props.schema) && _.has(this.props.schema, 'name') ? this.props.schema.name : null
  },
  _getTitle: function () {
    // todo if neither exist, use schema key (pass from parent as another prop?)
    return _.isString(this.props.title) ? this.props.title : _.isObject(this.props.schema) && _.has(this.props.schema, 'title') ? this.props.schema.title : this.props.name
  },
  _getValues: function () {
    let schema = this.props.schema
    return _.isArray(this.props.values) ? this.props.values : // use values if passed
    schema && schema.type === 'boolean' ? [true, false] : // if type boolean, values are true/false
    schema && schema['enum'] ? schema['enum'] : // enumerated values
    schema && schema.oneOf && // another way of enumerating values, which puts the labels in the schema instead
    _.every(schema.oneOf, function) {
      return _.has(s, 'enum') && s['enum'].length == 1
    }) ? schema.oneOf.map(function ) {
      return aSchema['enum'][0]
    }) : // todo: deal with labels for this type
    null
  },
  _getSelectedValues: function () {
    return _.isObject(this.props.filter) && _.has(this.props.filter, 'intersects') ? this.props.filter.intersects : []
  },

  onClickCheckbox: function (value, e) {
    let selectedValues = this._getSelectedValues().slice() // copy so we don't modify props
    let valueIndex = _.indexOf(selectedValues, value)
    valueIndex > -1 ? selectedValues.splice(valueIndex, 1) : selectedValues.push(value)
    let newFilter = selectedValues.length ? { intersects: selectedValues } : null
    this.props.onChange(newFilter)
  },

  render: function () {
    let _this = this

    let name = this._getName()
    let values = this._getValues()
    let selectedValues = this._getSelectedValues()
    let schema = this.props.schema

    return React.createElement(
      'div',
      { className: 'ds-checkbox-filter' },
      React.createElement(
        'div',
        { className: 'ds-checkbox-filter-title' },
        this._getTitle()
        ),
      values.map(function , i) {
        let hasLabelValue = _.has(listValue, 'label') && _.has(listValue, 'label')

        let _ref = hasLabelValue ? listValue : { label: listValue, value: listValue }

        let label = _ref.label
        let value = _ref.value

        if (!hasLabelValue && schema && schema.oneOf && schema.oneOf[i]) label = schema.oneOf[i].title || label

          let isSelected = _.indexOf(selectedValues, value) > -1
        return React.createElement(
          'label',
          null,
          React.createElement('input', { type: 'checkbox',
            name: name,
            value: value,
            checked: isSelected,
            onClick: _this.onClickCheckbox.bind(null, value)
          }),
          label
          )
      })
      )
  }
})

export default FilterInputCheckbox
