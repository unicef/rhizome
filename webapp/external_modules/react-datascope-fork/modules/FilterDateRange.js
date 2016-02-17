import _ from 'lodash'
import React from 'react/addons'
import reactWidgetsLibDateTimePicker from 'react-widgets/lib/DateTimePicker'


FilterDateRange = React.createClass({
    displayName: 'FilterDateRange',
    propTypes: {
        name: React.PropTypes.string,
        schema: React.PropTypes.object,
        filter: React.PropTypes.object,
        onChange: React.PropTypes.func,
        // include the minimum (after) part of the time range
        hasMin: React.PropTypes.bool,
        // include the maximum (before) part of the time range
        hasMax: React.PropTypes.bool,
        showTitle: React.PropTypes.bool,
        preMinContent: React.PropTypes.node,
        postMinContent: React.PropTypes.node,
        preMaxContent: React.PropTypes.node,
        postMaxContent: React.PropTypes.node,
        calendar: React.PropTypes.bool, // whether to show the date picker button
        time: React.PropTypes.bool // whether to show the time picker button
    },
    getDefaultProps: function () {
        return {
            showTitle: true,
            hasMin: true,
            hasMax: true
        }
    },

    componentWillMount: function () {
        this._validateProps()
    },
    componentWillReceiveProps: function () {
        this._validateProps()
    },
    _validateProps: function () {
        let schema = this.props.schema

        if (!_.isObject(schema)) throw 'FilterDateRange requires a schema (wrap this component in FilterPanel)'
        if (schema.type !== 'string' || schema.format !== 'date-time') throw 'FilterDateRange data schema must be type: \'string\' and format: \'date-time\''
    },

    _getTitle: function () {
        // todo if neither exist, use schema key (pass from parent as another prop?)
        return _.isString(this.props.title) ? this.props.title : _.isObject(this.props.schema) && _.has(this.props.schema, 'title') ? this.props.schema.title : this.props.name
    },

    onChangeDate: function (date, dateString) {
        let newFilter = { gt: date }
        this.props.onChange(newFilter)
    },

    onClickCheckbox: function (value, e) {
        let selectedValues = this._getSelectedValues().slice() // copy so we don't modify props
        let valueIndex = _.indexOf(selectedValues, value)
        valueIndex > -1 ? selectedValues.splice(valueIndex, 1) : selectedValues.push(value)
        let newFilter = selectedValues.length ? { intersects: selectedValues } : null
        this.props.onChange(this._getName(), newFilter)
    },

    onChangeMinDate: function (minDate) {
        let newFilter = this.props.filter ? _.clone(this.props.filter) : {}
        if (!minDate) delete newFilter.gtelse _.assign(newFilter, { gt: minDate })
        this.props.onChange(newFilter)
    },

    onChangeMaxDate: function (maxDate) {
        let newFilter = this.props.filter ? _.clone(this.props.filter) : {}
        if (!maxDate) delete newFilter.ltelse _.assign(newFilter, { lt: maxDate })
        this.props.onChange(newFilter)
    },

    render: function () {
        let _props = this.props
        let hasMin = _props.hasMin
        let hasMax = _props.hasMax
        let showTitle = _props.showTitle
        let calendar = _props.calendar
        let time = _props.time
        let preMinContent = _props.preMinContent
        let postMinContent = _props.postMinContent
        let preMaxContent = _props.preMaxContent
        let postMaxContent = _props.postMaxContent

        let hasContent = !_.every(preMinContent, postMinContent, preMaxContent, postMaxContent, _.isUndefined)

        if (!hasContent && hasMin && hasMax) {
            preMinContent = React.createElement(
                'span',
                { className: 'ds-date-range-pre-min' },
                'Between'
            )
            preMaxContent = React.createElement(
                'span',
                { className: 'ds-date-range-pre-max' },
                'and'
            )
        } else if (!hasContent) {
            preMinContent = React.createElement(
                'span',
                { className: 'ds-date-range-pre-min' },
                'Before'
            )
            preMaxContent = React.createElement(
                'span',
                { className: 'ds-date-range-pre-min' },
                'After'
            )
        }

        let pickerProps = { calendar: calendar, time: time }

        let titleContent = showTitle ? React.createElement(
            'div',
            { className: 'ds-date-range-title' },
            this._getTitle()
        ) : null

        let minContent = hasMin ? React.createElement(
            'div',
            { className: 'ds-date-range-min' },
            preMinContent,
            React.createElement(reactWidgetsLibDateTimePicker, _extends({
                onChange: this.onChangeMinDate,
                value: this.props.filter && this.props.filter.gt || null
            }, pickerProps)),
            postMinContent
        ) : null

        let maxContent = hasMax ? React.createElement(
            'div',
            { className: 'ds-date-range-max' },
            preMaxContent,
            React.createElement(reactWidgetsLibDateTimePicker, _extends({
                onChange: this.onChangeMaxDate,
                value: this.props.filter && this.props.filter.lt || null
            }, pickerProps)),
            postMaxContent
        ) : null

        return React.createElement(
            'div',
            { className: 'ds-date-range-filter' },
            titleContent,
            minContent,
            maxContent
        )
    }
})
let _extends = Object.assign || function (target) { for (let i = 1 i < arguments.length i++) { let source = arguments[i] for (let key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key] } } } return target }

export default FilterDateRange
