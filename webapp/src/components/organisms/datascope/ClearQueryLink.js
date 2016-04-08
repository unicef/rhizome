'use strict';

Object.defineProperty(exports, '__esModule', {
    value: true
});

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _lodash = require('lodash');

var _lodash2 = _interopRequireDefault(_lodash);

var _reactAddons = require('react/addons');

var _reactAddons2 = _interopRequireDefault(_reactAddons);

var _InterfaceMixin = require('utilities/InterfaceMixin');

// import InterfaceMixin from ''


var _InterfaceMixin2 = _interopRequireDefault(_InterfaceMixin);

// Datascope module which clears existing filters, searches and sorts, and resets to first page
// (each type can be selectively disabled with clearWhatever = false)
// renders children wrapped in a clickable div

var ClearQueryLink = _reactAddons2['default'].createClass({
    displayName: 'ClearQueryLink',

    mixins: [(0, _InterfaceMixin2['default'])('Datascope')],
    propTypes: {
        clearFilters: _reactAddons2['default'].PropTypes.bool,
        clearSearch: _reactAddons2['default'].PropTypes.bool,
        clearSort: _reactAddons2['default'].PropTypes.bool,
        clearPagination: _reactAddons2['default'].PropTypes.bool
    },
    getDefaultProps: function getDefaultProps() {
        return {
            clearFilters: true,
            clearSearch: true,
            clearSort: true,
            clearPagination: true
        };
    },

    onClick: function onClick() {
        var _props = this.props;
        var clearFilters = _props.clearFilters;
        var clearSearch = _props.clearSearch;
        var clearSort = _props.clearSort;
        var clearPagination = _props.clearPagination;

        var query = this.props.query;

        if (clearFilters) query = _reactAddons2['default'].addons.update(query, { filter: { $set: undefined } });
        if (clearSearch) query = _reactAddons2['default'].addons.update(query, { search: { $set: undefined } });
        if (clearSort) query = _reactAddons2['default'].addons.update(query, { sort: { $set: undefined } });
        if (clearPagination && query.pagination) query = _reactAddons2['default'].addons.update(query, { pagination: { $merge: { page: 1, offset: 0 } } });

        this.props.onChangeQuery(query);
        //return false;
    },

    render: function render() {
        var content = this.props.children || 'Clear filters';

        return _reactAddons2['default'].createElement(
            'div',
            { className: 'ds-clear-query-link', onClick: this.onClick },
            content
        );
    }
});

exports['default'] = ClearQueryLink;
module.exports = exports['default'];
