import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from 'components/molecules/NavMenuItem.jsx'
import RootStore from 'stores/RootStore'

let DashboardNav = React.createClass({

  mixins: [
    Reflux.connect(RootStore),
    require('components/molecules/menus/MenuControl')
  ],

  render: function () {
    let dashboards = this.state.dashboards

    if (!_.isUndefined(dashboards) && dashboards.length > 14) {
      dashboards = _.slice(dashboards, 0, 14)
    }

    const premade_dashboards = dashboards.map(dashboard => {
      if (dashboard.builtin && dashboard.dashboardType === 'EocCampaign') {
        return (
          <NavMenuItem key={dashboard.id} href={'/dashboards/' + _.kebabCase(dashboard.title)}>
            {dashboard.title}
          </NavMenuItem>
        )
      }
    })

    const custom_charts = this.state.charts.map(chart =>
      <NavMenuItem key={chart.chart_json.id} href={'/charts/' + chart.id}>
        { chart.title }
      </NavMenuItem>
    )

    return (
      <ul className='dashboards-nav'>
        <li>
          <a href='#'>Charts</a>
          <ul className='dashboard-menu'>
            { custom_charts }
            <li className='separator'><hr /></li>
            <li><a href='/charts/create'>Create a Chart</a></li>
          </ul>
        </li>
        <li>
          <a href='#'>Dashboards</a>
          <ul className='dashboard-menu'>
            { premade_dashboards }
          </ul>
        </li>
        <li className='log-out'>
          <a href='/accounts/logout?next=/' title='logout'>
            Log Out &nbsp;
            <i className='fa fa-lg fa-sign-out'/>
          </a>
        </li>
      </ul>
    )
  }
})

export default DashboardNav
