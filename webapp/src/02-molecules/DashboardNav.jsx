import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from '02-molecules/NavMenuItem.jsx'
import NavigationStore from 'stores/NavigationStore'

export default React.createClass({
  mixins: [
    Reflux.connect(NavigationStore),
    require('02-molecules/menus/MenuControl')
  ],

  render: function () {
    var dashboards = this.state.dashboards
    var builtins = NavMenuItem.fromArray(_(dashboards)
        .filter(d => (d.builtin && d.id !== -4 && d.title.indexOf('Homepage') === -1))
        .map(function (d) {
          return _.assign({
            key: 'dashboard-nav-' + d.id
          }, d)
        })
        .value()
      )

    if (!_.isUndefined(dashboards)) {
      if (dashboards.length > 14) {
        dashboards = _.slice(dashboards, 0, 14)
      }
    }

    var customDashboards = NavMenuItem.fromArray(_(dashboards)
      .filter(d => !d.builtin)
      .map(function (d) {
        return _.assign({
          key: 'dashboard-nav-' + d.id
        }, d)
      })
      .value()
    )

    var customCharts = []

    return (
      <ul className='dashboards-nav'>
        <li className='small-4 columns'>
          <a href='/datapoints/dashboards/'>Dashboards</a>
          <ul className='dashboard-menu'>
            <li className='main-item'>
              <a href='/datapoints/dashboards/create'>Create a dashboard</a>
            </li>
            {builtins}
            <li className='separator'>
              <hr />
            </li>
            {customDashboards}
          </ul>
        </li>
        <li className='small-4 columns'>
          <a href='/datapoints/charts/'>Charts</a>
          <ul className='dashboard-menu'>
            <li className='main-item'>
              <a href='/datapoints/charts/create'>Create a chart</a>
            </li>
            {customCharts}
          </ul>
        </li>
        <li className='small-4 columns log-out'>
          <a href='/accounts/logout?next=/' title='logout'>
            <i className='fa fa-lg fa-sign-out'/><br />log out
          </a>
        </li>
      </ul>
    )
  }
})
