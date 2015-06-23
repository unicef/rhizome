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

  render : function () {
    var region = this.props.selected.name;

    var filter  = this.state.filter;

    var regions = _.map(this.props.regions, function (r) {
      return {
        title  : r.name,
        value  : r.id,
        parent : r.parent_region_id
      };
    });

    if (_.size(filter) > 2) {
      var re = new RegExp(filter, 'gi');

      regions = _.filter(regions, r => re.test(r.title));
    } else {
      var idx = _.indexBy(regions, 'value');

      regions = [];
      _.each(idx, function (region) {
        if (idx.hasOwnProperty(region.parent)) {
          var p        = idx[region.parent];
          var children = _.get(p, 'children', []);

          children.push(region);

          // Ew… resorting on every iteration…
          p.children = _.sortBy(children, 'title');
        } else {
          regions.push(region);
        }
      });
    }

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
  }
});

module.exports = RegionTitleMenu;
