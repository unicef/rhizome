'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _lodash = require('lodash');

var _lodash2 = _interopRequireDefault(_lodash);

var _reactAddons = require('react/addons');

var _reactAddons2 = _interopRequireDefault(_reactAddons);

var _reactWidgetsLibDateTimePicker = require('react-widgets/lib/DateTimePicker');

var _reactWidgetsLibDateTimePicker2 = _interopRequireDefault(_reactWidgetsLibDateTimePicker);

var PropTypes = _reactAddons2['default'].PropTypes;
exports['default'] = _reactAddons2['default'].createClass({
    displayName: 'FilterDateRange',
    propTypes: {
        name: PropTypes.string,
        schema: PropTypes.object,
        filter: PropTypes.object,
        onChange: PropTypes.func,
        // include the minimum (after) part of the time range
        hasMin: PropTypes.bool,
        // include the maximum (before) part of the time range
        hasMax: PropTypes.bool,
        showTitle: PropTypes.bool,
        preMinContent: PropTypes.node,
        postMinContent: PropTypes.node,
        preMaxContent: PropTypes.node,
        postMaxContent: PropTypes.node,
        calendar: PropTypes.bool, // whether to show the date picker button
        time: PropTypes.bool // whether to show the time picker button
    },
    getDefaultProps: function getDefaultProps() {
        return {
            showTitle: true,
            hasMin: true,
            hasMax: true
        };
    },

    componentWillMount: function componentWillMount() {
        this._validateProps();
    },
    componentWillReceiveProps: function componentWillReceiveProps() {
        this._validateProps();
    },
    _validateProps: function _validateProps() {
        var schema = this.props.schema;

        if (!_lodash2['default'].isObject(schema)) throw 'FilterDateRange requires a schema (wrap this component in FilterPanel)';
        if (schema.type !== 'string' || schema.format !== 'date-time') throw 'FilterDateRange data schema must be type: \'string\' and format: \'date-time\'';
    },

    _getTitle: function _getTitle() {
        // todo if neither exist, use schema key (pass from parent as another prop?)
        return _lodash2['default'].isString(this.props.title) ? this.props.title : _lodash2['default'].isObject(this.props.schema) && _lodash2['default'].has(this.props.schema, 'title') ? this.props.schema.title : this.props.name;
    },

    onChangeDate: function onChangeDate(date, dateString) {
        var newFilter = { gt: date };
        this.props.onChange(newFilter);
    },
    onClickCheckbox: function onClickCheckbox(value, e) {
        var selectedValues = this._getSelectedValues().slice(); // copy so we don't modify props
        var valueIndex = _lodash2['default'].indexOf(selectedValues, value);
        valueIndex > -1 ? selectedValues.splice(valueIndex, 1) : selectedValues.push(value);
        var newFilter = selectedValues.length ? { intersects: selectedValues } : null;
        this.props.onChange(this._getName(), newFilter);
    },

    onChangeMinDate: function onChangeMinDate(minDate) {
        var newFilter = this.props.filter ? _lodash2['default'].clone(this.props.filter) : {};
        if (!minDate) delete newFilter.gt;else _lodash2['default'].assign(newFilter, { gt: minDate });
        this.props.onChange(newFilter);
    },
    onChangeMaxDate: function onChangeMaxDate(maxDate) {
        var newFilter = this.props.filter ? _lodash2['default'].clone(this.props.filter) : {};
        if (!maxDate) delete newFilter.lt;else _lodash2['default'].assign(newFilter, { lt: maxDate });
        this.props.onChange(newFilter);
    },

    render: function render() {
        var _props = this.props;
        var hasMin = _props.hasMin;
        var hasMax = _props.hasMax;
        var showTitle = _props.showTitle;
        var calendar = _props.calendar;
        var time = _props.time;
        var preMinContent = _props.preMinContent;
        var postMinContent = _props.postMinContent;
        var preMaxContent = _props.preMaxContent;
        var postMaxContent = _props.postMaxContent;

        var hasContent = !_lodash2['default'].every(preMinContent, postMinContent, preMaxContent, postMaxContent, _lodash2['default'].isUndefined);

        if (!hasContent && hasMin && hasMax) {
            preMinContent = _reactAddons2['default'].createElement(
                'span',
                { className: 'ds-date-range-pre-min' },
                'Between'
            );
            preMaxContent = _reactAddons2['default'].createElement(
                'span',
                { className: 'ds-date-range-pre-max' },
                'and'
            );
        } else if (!hasContent) {
            preMinContent = _reactAddons2['default'].createElement(
                'span',
                { className: 'ds-date-range-pre-min' },
                'Before'
            );
            preMaxContent = _reactAddons2['default'].createElement(
                'span',
                { className: 'ds-date-range-pre-min' },
                'After'
            );
        }

        var pickerProps = { calendar: calendar, time: time };

        var titleContent = showTitle ? _reactAddons2['default'].createElement(
            'div',
            { className: 'ds-date-range-title' },
            this._getTitle()
        ) : null;

        var minContent = hasMin ? _reactAddons2['default'].createElement(
            'div',
            { className: 'ds-date-range-min' },
            preMinContent,
            _reactAddons2['default'].createElement(_reactWidgetsLibDateTimePicker2['default'], _extends({
                onChange: this.onChangeMinDate,
                value: this.props.filter && this.props.filter.gt || null
            }, pickerProps)),
            postMinContent
        ) : null;

        var maxContent = hasMax ? _reactAddons2['default'].createElement(
            'div',
            { className: 'ds-date-range-max' },
            preMaxContent,
            _reactAddons2['default'].createElement(_reactWidgetsLibDateTimePicker2['default'], _extends({
                onChange: this.onChangeMaxDate,
                value: this.props.filter && this.props.filter.lt || null
            }, pickerProps)),
            postMaxContent
        ) : null;

        return _reactAddons2['default'].createElement(
            'div',
            { className: 'ds-date-range-filter' },
            titleContent,
            minContent,
            maxContent
        );
    }
});

//export default FilterDateRange;
module.exports = exports['default'];
