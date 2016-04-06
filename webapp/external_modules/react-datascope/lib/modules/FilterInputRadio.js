'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _lodash = require('lodash');

var _lodash2 = _interopRequireDefault(_lodash);

var _reactAddons = require('react/addons');

var _reactAddons2 = _interopRequireDefault(_reactAddons);

var PropTypes = _reactAddons2['default'].PropTypes;

var RadioGroup = _reactAddons2['default'].createClass({
    displayName: 'RadioGroup',

    render: function render() {
        var _this = this;

        return _reactAddons2['default'].createElement(
            'div',
            _lodash2['default'].omit(this.props, 'onChange'),
            _reactAddons2['default'].Children.map(this.props.children, function (child) {
                var propsToPass = _lodash2['default'].pick(_this.props, 'name');
                propsToPass.checked = _this.props.value !== null && _this.props.value === child.props.value;
                propsToPass.onClick = _this.props.onChange.bind(null, child.props.value);
                return _reactAddons2['default'].cloneElement(child, propsToPass);
            })
        );
    }
});

var FilterInputRadio = _reactAddons2['default'].createClass({
    displayName: 'FilterInputRadio',

    propTypes: {
        // schema describing the field
        schemaold: PropTypes.shape({
            name: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
            title: PropTypes.string,
            type: PropTypes.string,
            constraints: PropTypes.shape({
                oneOf: PropTypes.array
            })
        }),

        schema: PropTypes.object,

        filter: PropTypes.object,

        // provide name, label, values optionally to override the schema
        // unique name for this collection of radio buttons (for name attribute)
        name: PropTypes.string,
        // human-readable label for this collection of radio buttons
        label: PropTypes.string,
        // list of possible values for the radio buttons, in one of two formats:
        // ['val1', 'val2', 'val3', ...] // OR...
        // [{label: "Value 1", value: 'val1'}, {label: "Value 2", value: 'val2'}, ...]
        // if the former, array values will be used for both labels and input values
        values: PropTypes.array,

        // if true, clicking on a selected radio button will deselect it (unlike standard browser behavior)
        shouldDeselect: PropTypes.bool
    },
    getDefaultProps: function getDefaultProps() {
        return { shouldDeselect: true };
    },
    componentWillMount: function componentWillMount() {
        this._validateProps();
    },
    componentWillReceiveProps: function componentWillReceiveProps() {
        this._validateProps();
    },

    _validateProps: function _validateProps() {
        if (!this.props.name) throw 'FilterInputRadio requires a `name` prop';
        if (_lodash2['default'].isNull(this._getValues())) throw 'FilterInputRadio requires valid schema or `values` prop';
    },
    _getTitle: function _getTitle() {
        // todo if neither exist, use schema key (pass from parent as another prop?)
        return _lodash2['default'].isString(this.props.title) ? this.props.title : _lodash2['default'].isObject(this.props.schema) && _lodash2['default'].has(this.props.schema, 'title') ? this.props.schema.title : this.props.name;
    },
    _getValues: function _getValues() {
        var schema = this.props.schema;
        return _lodash2['default'].isArray(this.props.values) ? this.props.values : // use values if passed
        schema && schema.type === 'boolean' ? [true, false] : // if type boolean, values are true/false
        schema && schema['enum'] ? schema.type['enum'] : // enumerated values
        schema && schema.oneOf && // another way of enumerating values, which puts the labels in the schema instead
        _lodash2['default'].every(schema.oneOf, function (s) {
            return _lodash2['default'].has(s, 'enum') && s['enum'].length == 1;
        }) ? schema.oneOf.map(function (aSchema) {
            return aSchema['enum'][0];
        }) : // todo: deal with labels for this type
        null;
    },
    _getSelectedValue: function _getSelectedValue() {
        return _lodash2['default'].isObject(this.props.filter) && _lodash2['default'].has(this.props.filter, 'eq') ? this.props.filter.eq : null;
    },

    onClickRadio: function onClickRadio(value, e) {
        var newFilter = this.props.shouldDeselect && value === this._getSelectedValue() ? {} : { eq: value };
        this.props.onChange(newFilter);
    },

    render: function render() {
        var value = this._getSelectedValue();

        return _reactAddons2['default'].createElement(
            'div',
            { className: 'ds-radio-filter' },
            _reactAddons2['default'].createElement(
                'div',
                { className: 'ds-radio-filter-title' },
                this._getTitle()
            ),
            _reactAddons2['default'].createElement(
                RadioGroup,
                {
                    className: 'ds-radio-group',
                    ref: 'group',
                    name: this.props.name,
                    value: value,
                    onChange: this.onClickRadio
                },
                this._getValues().map(function (value) {
                    var label = (_lodash2['default'].has(value, 'label') ? value.label : value) + '';
                    value = _lodash2['default'].has(value, 'value') ? value.value : value;
                    return _reactAddons2['default'].createElement(
                        'input',
                        {
                            className: 'ds-radio-input',
                            type: 'radio',
                            value: value
                        },
                        _reactAddons2['default'].createElement(
                            'span',
                            { className: 'ds-radio-input-label' },
                            label
                        )
                    );
                })
            )
        );
    }
});

exports['default'] = FilterInputRadio;
module.exports = exports['default'];
