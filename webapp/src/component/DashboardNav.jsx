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
    var dashboards = this.state.dashboards;

    var builtins = NavMenuItem.fromArray(_(dashboards)
      .filter(d=>d.builtin)
      .map(function(d) {
        return _.assign({
          key: 'dashboard-nav-' + d.id
        }, d);
      })
      .value()
    );

    if (!_.isUndefined(dashboards)) {
      if (dashboards.length>14) {
        dashboards = _.slice(dashboards,0,14);
      }
    }

    var customDashboards = NavMenuItem.fromArray(_(dashboards)
      .filter(d=>!d.builtin)
      .map(function(d) {
        return _.assign({
          key: 'dashboard-nav-' + d.id
        }, d);
      })
      .value()
    );

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
