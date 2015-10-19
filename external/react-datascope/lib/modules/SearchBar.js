'use strict';

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _ = require('lodash'),
    React = require('react/addons'),
    InterfaceMixin = require('./../InterfaceMixin');

var SearchBar = React.createClass({
    displayName: 'SearchBar',

    mixins: [InterfaceMixin('Datascope', 'DatascopeSearch')],
    propTypes: {
        onChangeSearch: React.PropTypes.func, // required
        id: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
        fieldNames: React.PropTypes.array,
        value: React.PropTypes.string
    },

    getDefaultProps: function getDefaultProps() {
        return {
            id: 'searchbar' // pass unique id to have multiple independent search bars within one Datascope
        };
    },

    onChangeSearch: function onChangeSearch(e) {
        this.props.onChangeSearch(this.props.id, e.target.value, this.props.fieldNames);
    },

    render: function render() {
        var propsToPass = _.omit(this.props, ['id', 'fieldNames', 'value', 'onChangeSearch']);
        return React.createElement(
            'div',
            null,
            React.createElement('input', _extends({
                type: 'text',
                value: this.props.value,
                onChange: this.onChangeSearch
            }, propsToPass))
        );
    }
});

module.exports = SearchBar;
