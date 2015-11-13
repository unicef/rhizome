'use strict'

import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from 'component/NavMenuItem.jsx'
import NavigationStore from 'stores/NavigationStore'

module.exports = React.createClass({
  mixins: [
    Reflux.connect(NavigationStore),
    require('mixin/MenuControl')
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

    return (
      <ul className='dashboards-nav'>
        <li className='small-4 columns'>
          <a>View My<br />Dashboards</a>
          <ul className='dashboard-menu'>
            {builtins}
            <li className='separator'>
              <hr />
            </li>
            {customDashboards}
            <li className='allCustomDashboards'>
                <a role='menuitem' href='/datapoints/dashboards/' tabIndex='-1'>
                  See all custom dashboards
                </a>
              </li>
          </ul>
        </li>
        <li className='small-4 columns'>
          <a href='/datapoints/dashboards/edit'>Create a<br />dashboard</a>
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
