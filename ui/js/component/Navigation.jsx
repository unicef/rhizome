'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');

var NavMenu         = require('component/NavMenu.jsx');
var NavMenuItem     = require('component/NavMenuItem.jsx');
var NavigationStore = require('stores/NavigationStore');

var Navigation = React.createClass({
  mixins : [
    Reflux.connect(NavigationStore)
  ],

  render : function () {
    var dashboards = NavMenuItem.fromArray(_.map(this.state.dashboards, function (d) {
      return _.assign({ key : 'dashboard-nav-' + d.id }, d);
    }));

    return (
      <nav>
        <ul>
          <li className='home'><a href='/'>
            <i className='fa fa-home fa-lg'></i>&ensp;Home
          </a></li>

          <li className='dashboard'>
            <NavMenu text={'Explore Data'} icon={'fa-bar-chart'}>
              {dashboards}
              <li className='separator'><hr /></li>
              <NavMenuItem href='/datapoints/table'>Data Browser</NavMenuItem>
              <li className='separator'><hr /></li>
              <NavMenuItem href='/datapoints/dashboard/'>
                See all custom dashboards
              </NavMenuItem>
              <NavMenuItem href='/datapoints/dashboard/create'>
                Create New dashboard
              </NavMenuItem>
            </NavMenu>
          </li>

          <li className='data'>
            <NavMenu text={'Enter Data'} icon={'fa-table'}>
              <NavMenuItem href='/datapoints/entry'>
                Edit Data
              </NavMenuItem>
              <NavMenuItem href='/upload'>
                Upload Data
              </NavMenuItem>
            </NavMenu>
          </li>

          <li><a href='/ufadmin/users'>
            <i className='fa fa-cogs'></i>&ensp;Manage System
          </a></li>
        </ul>

        <ul className='right'>
          <li>
            <a href='/accounts/logout?next=/' title='logout'>
              log out&ensp;<i className='fa fa-lg fa-sign-out'></i>
            </a>
          </li>
        </ul>
      </nav>
    );
  }
});

module.exports = Navigation;
