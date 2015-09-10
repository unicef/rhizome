'use strict';

var _     = require('lodash');
var React = require('react');

var TitleMenu = require('component/TitleMenu.jsx');
var MenuItem  = require('component/MenuItem.jsx');

var RegionTitleMenu = React.createClass({
  propTypes : {
    regions   : React.PropTypes.array.isRequired,
    selected  : React.PropTypes.object.isRequired,
    sendValue : React.PropTypes.func.isRequired
  },

  getInitialState : function () {
    return {
      filter : ''
    };
  },
  shouldComponentUpdate: function(nextProps, nextState) {

      return (nextProps.regions.length !== this.props.regions.length || nextProps.selected.id !==this.props.selected.id);
  },

  render : function () {
    var region = this.props.selected.name;

    var filter  = this.state.filter;

    var regions = this._buildRegions(this.props.regions, filter)

    var items = MenuItem.fromArray(_.sortBy(regions, 'title'), this.props.sendValue);

    return (
      <TitleMenu
        icon='fa-globe'
        text={region}
        searchable={true}
        onSearch={this._setFilter}>
        {items}
      </TitleMenu>
    );
  },

  _setFilter : function (pattern) {
    this.setState({ filter : pattern })
  },

  _buildRegions: function(originalRegions, filter) {
    var regions = originalRegions.map(r => {
      return {
        title  : r.name,
        value  : r.id,
        parent : r.parent_region_id
      };
    });

    if (filter.length > 2) {
      regions = regions.filter(r => {
        return new RegExp(filter, 'i').test(r.title)
      })
    } else {
      var idx = _.indexBy(regions, 'value');
      regions = [];
      _.each(idx, region => {
        if (idx.hasOwnProperty(region.parent)) {
          var p = idx[region.parent];
          var children = p.children || []

          children.push(region);
          p.children = _.sortBy(children, 'title');
        } else {
          regions.push(region);
        }
      });
    }

    return regions
  }
});

module.exports = RegionTitleMenu;
