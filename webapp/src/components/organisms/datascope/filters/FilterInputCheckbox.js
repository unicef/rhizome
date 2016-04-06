'use strict';

var _ = require('lodash'),
    React = require('react/addons');

var PropTypes = React.PropTypes;

var FilterInputCheckbox = React.createClass({
    displayName: 'FilterInputCheckbox',

    propTypes: {
        // schema describing the field
        schema: PropTypes.shape({
            name: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
            title: PropTypes.string,
            type: PropTypes.string,
            constraints: PropTypes.shape({
                oneOf: PropTypes.array,
                items: PropTypes.shape({
                    oneOf: PropTypes.array
                })
            })
        }),
        filter: PropTypes.object,

        // provide name, label, values to override the schema
        // unique name for this collection of checkboxes (for name attribute)
        name: PropTypes.string,
        // human-readable label for this collection of checkboxes
        label: PropTypes.string,
        // list of possible values for the checkboxes, in one of two formats:
        // ['val1', 'val2', 'val3', ...] // OR...
        // [{label: "Value 1", value: 'val1'}, {label: "Value 2", value: 'val2'}, ...]
        // if the former, array values will be used for both labels and input values
        values: PropTypes.array
    },
    componentWillMount: function componentWillMount() {
        this._validateProps();
    },
    componentWillReceiveProps: function componentWillReceiveProps() {
        this._validateProps();
    },

    _validateProps: function _validateProps() {
        if (_.isNull(this._getName())) throw 'FilterInputCheckbox requires schema or `name` prop';
        if (_.isNull(this._getValues())) throw 'FilterInputCheckbox requires schema or `values` prop';
    },
    _getName: function _getName() {
        return _.isString(this.props.name) ? this.props.name : _.isObject(this.props.schema) && _.has(this.props.schema, 'name') ? this.props.schema.name : null;
    },
    _getTitle: function _getTitle() {
        // todo if neither exist, use schema key (pass from parent as another prop?)
        return _.isString(this.props.title) ? this.props.title : _.isObject(this.props.schema) && _.has(this.props.schema, 'title') ? this.props.schema.title : this.props.name;
    },
    _getValues: function _getValues() {
        var schema = this.props.schema;
        return _.isArray(this.props.values) ? this.props.values : // use values if passed
        schema && schema.type === 'boolean' ? [true, false] : // if type boolean, values are true/false
        schema && schema['enum'] ? schema['enum'] : // enumerated values
        schema && schema.oneOf && // another way of enumerating values, which puts the labels in the schema instead
        _.every(schema.oneOf, function (s) {
            return _.has(s, 'enum') && s['enum'].length == 1;
        }) ? schema.oneOf.map(function (aSchema) {
            return aSchema['enum'][0];
        }) : // todo: deal with labels for this type
        null;
    },
    _getSelectedValues: function _getSelectedValues() {
        return _.isObject(this.props.filter) && _.has(this.props.filter, 'intersects') ? this.props.filter.intersects : [];
    },

    onClickCheckbox: function onClickCheckbox(value, e) {
        var selectedValues = this._getSelectedValues().slice(); // copy so we don't modify props
        var valueIndex = _.indexOf(selectedValues, value);
        valueIndex > -1 ? selectedValues.splice(valueIndex, 1) : selectedValues.push(value);
        var newFilter = selectedValues.length ? { intersects: selectedValues } : null;
        this.props.onChange(newFilter);
    },

    render: function render() {
        var _this = this;

        var name = this._getName();
        var values = this._getValues();
        var selectedValues = this._getSelectedValues();
        var schema = this.props.schema;

        return React.createElement(
            'div',
            { className: 'ds-checkbox-filter' },
            React.createElement(
                'div',
                { className: 'ds-checkbox-filter-title' },
                this._getTitle()
            ),
            values.map(function (listValue, i) {
                var hasLabelValue = _.has(listValue, 'label') && _.has(listValue, 'label');

                var _ref = hasLabelValue ? listValue : { label: listValue, value: listValue };

                var label = _ref.label;
                var value = _ref.value;

                if (!hasLabelValue && schema && schema.oneOf && schema.oneOf[i]) label = schema.oneOf[i].title || label;

                var isSelected = _.indexOf(selectedValues, value) > -1;
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
                );
            })
        );
    }
});

module.exports = FilterInputCheckbox;
//return value.label
