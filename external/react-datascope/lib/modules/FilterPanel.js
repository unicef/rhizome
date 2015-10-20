'use strict';

var _ = require('lodash'),
    React = require('react/addons'),
    InterfaceMixin = require('./../InterfaceMixin'),
    FilterInputRadio = require('./FilterInputRadio');

var PropTypes = React.PropTypes;

var FilterPanel = React.createClass({
    displayName: 'FilterPanel',

    mixins: [InterfaceMixin('Datascope', 'DatascopeFilter')],
    propTypes: {
        filter: React.PropTypes.objectOf(React.PropTypes.object),
        fields: React.PropTypes.array,
        schema: React.PropTypes.object
    },
    getDefaultProps: function getDefaultProps() {
        return {
            filter: {},
            schema: {},
            testing: 4
        };
    },

    onChangeFilterInput: function onChangeFilterInput(key, filterObj) {
        this.props.onChangeFilter(key, filterObj);
    },

    render: function render() {
        var propSchemas = this.props.schema.items.properties;
        return React.createElement(
            'div',
            { className: 'datascope-filter-panel' },
            this.recursiveCloneChildren(this.props.children)
        );
    },
    recursiveCloneChildren: function recursiveCloneChildren(children) {
        var _this = this;

        return React.Children.map(children, function (child) {
            if (!_.isObject(child)) return child;

            var childProps = {};
            var isFilter = child.props && child.props.name;
            if (isFilter) {
                var childKey = child.props.name;
                var propSchemas = _this.props.schema.items.properties;
                childProps = {
                    schema: propSchemas[childKey],
                    filter: _this.props.filter[childKey],
                    onChange: _this.onChangeFilterInput.bind(_this, childKey)
                };
            }

            if (child.props.children) childProps.children = _this.recursiveCloneChildren(child.props.children);

            return React.cloneElement(child, childProps);
        });
    }
});

module.exports = FilterPanel;
