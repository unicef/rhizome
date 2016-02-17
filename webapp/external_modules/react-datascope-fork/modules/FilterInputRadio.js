import _ from 'lodash'
import React from 'react/addons'
import RadioGroup from '02-molecules/datascope/modules/RadioGroup'

let FilterInputRadio = React.createClass({
  displayName: 'FilterInputRadio',

  propTypes: {
    // schema describing the field
    schemaold: React.PropTypes.shape({
      name: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
      title: React.PropTypes.string,
      type: React.PropTypes.string,
      constraints: React.PropTypes.shape({
        oneOf: React.PropTypes.array
      })
    }),
    schema: React.PropTypes.object,
    filter: React.PropTypes.object,
    // provide name, label, values optionally to override the schema
    // unique name for this collection of radio buttons (for name attribute)
    name: React.PropTypes.string,
    // human-readable label for this collection of radio buttons
    label: React.PropTypes.string,
    // list of possible values for the radio buttons, in one of two formats:
    // ['val1', 'val2', 'val3', ...] // OR...
    // [{label: "Value 1", value: 'val1'}, {label: "Value 2", value: 'val2'}, ...]
    // if the former, array values will be used for both labels and input values
    values: React.PropTypes.array,
    // if true, clicking on a selected radio button will deselect it (unlike standard browser behavior)
    shouldDeselect: React.PropTypes.bool,
    onChange: React.PropTypes.func
  },

  getDefaultProps: function () {
    return { shouldDeselect: true }
  },

  componentWillMount: function () {
    this._validateProps()
  },

  componentWillReceiveProps: function () {
    this._validateProps()
  },

  _validateProps: function () {
    if (!this.props.name) throw 'FilterInputRadio requires a `name` prop'
      if (_.isNull(this._getValues())) throw 'FilterInputRadio requires valid schema or `values` prop'
    },

  _getTitle: function () {
    // todo if neither exist, use schema key (pass from parent as another prop?)
    return _.isString(this.props.title) ? this.props.title : _.isObject(this.props.schema) && _.has(this.props.schema, 'title') ? this.props.schema.title : this.props.name
  },

  _getValues: function () {
    let schema = this.props.schema
    return _.isArray(this.props.values) ? this.props.values : // use values if passed
    schema && schema.type === 'boolean' ? [true, false] : // if type boolean, values are true/false
    schema && schema['enum'] ? schema.type['enum'] : // enumerated values
    schema && schema.oneOf && // another way of enumerating values, which puts the labels in the schema instead
    _.every(schema.oneOf, function (s) {
      return _.has(s, 'enum') && s['enum'].length == 1
    }) ? schema.oneOf.map(function (aSchema) {
      return aSchema['enum'][0]
    }) : // todo: deal with labels for this type
    null
  },

  _getSelectedValue: function () {
    return _.isObject(this.props.filter) && _.has(this.props.filter, 'eq') ? this.props.filter.eq : null
  },

  onClickRadio: function (value, e) {
    let newFilter = this.props.shouldDeselect && value === this._getSelectedValue() ? {} : { eq: value }
    this.props.onChange(newFilter)
  },

  render: function () {
    let value = this._getSelectedValue()

    return React.createElement(
      'div',
      { className: 'ds-radio-filter' },
      React.createElement(
        'div',
        { className: 'ds-radio-filter-title' },
        this._getTitle()
        ),
      React.createElement(
        RadioGroup,
        {
          className: 'ds-radio-group',
          ref: 'group',
          name: this.props.name,
          value: value,
          onChange: this.onClickRadio
        },
        this._getValues().map(function (value) {
          let label = (_.has(value, 'label') ? value.label : value) + ''
          value = _.has(value, 'value') ? value.value : value
          return React.createElement(
            'input',
            {
              className: 'ds-radio-input',
              type: 'radio',
              value: value
            },
            React.createElement(
              'span',
              { className: 'ds-radio-input-label' },
              label
              )
            )
        })
        )
      )
  }
})

export default FilterInputRadio
