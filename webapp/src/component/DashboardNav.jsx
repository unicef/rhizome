'use strict';

var _ = require('lodash');
var React = require('react');
var Reflux = require('reflux');

var NavMenu = require('component/NavMenu.jsx');
var NavMenuItem = require('component/NavMenuItem.jsx');
var NavigationStore = require('stores/NavigationStore');
var MenuControl = require('mixin/MenuControl');

module.exports = React.createClass({
  mixins: [
    Reflux.connect(NavigationStore),
    require('mixin/MenuControl')
  ],

  render : function () {
    var dashboards = NavMenuItem.fromArray(_(this.state.dashboards)
      .map(function(d) {
        return _.assign({
          key: 'dashboard-nav-' + d.id
        }, d);
      })
      .value()
    );

    var builtins = _.slice(dashboards,0,4);
    var customDashboards = _.slice(dashboards,4);

    if (customDashboards.length>10) {
      customDashboards = _.slice(customDashboards,0,10)
    }
    else {
    }

    return (
        <ul className="dashboards-nav">
          <li className="medium-4 columns">
          <a onClick={this._toggleMenu} tabIndex='-1'>View My Dashboards</a>
            <ul className="dashboard-menu">
              {builtins}
              <li className='separator'><hr /></li>
              {customDashboards}
              <NavMenuItem href='/datapoints/dashboards/'>
                See all custom dashboards
              </NavMenuItem>
            </ul>
          </li>
          <li className="medium-4 columns">
            <a href="/datapoints/dashboards/edit">Create a dashboard</a>
          </li>
          <li className="medium-4 columns">
            <a href='/accounts/logout?next=/' title='logout' className="lay-out">
              <i className='fa fa-lg fa-sign-out'/>
              log out
            </a>
          </li>
        </ul>
    );
  }
});
