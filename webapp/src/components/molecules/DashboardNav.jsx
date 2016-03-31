import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from 'components/molecules/NavMenuItem.jsx'
import ChartStore from 'stores/ChartStore'
import DashboardStore from 'stores/DashboardStore'
import RootStore from 'stores/RootStore'

let DashboardNav = React.createClass({

  mixins: [
    // Reflux.connect(RootStore),
    require('components/molecules/menus/MenuControl')
  ],

  getInitialState() {
    return {
      charts: [],
      dashboards: []
    }
  },

  componentDidMount () {
    ChartStore.listen(charts => this.setState({charts: charts.raw}))
    DashboardStore.listen(dashboards => this.setState({dashboards: dashboards.list}))
  },

  shouldComponentUpdate(nextProps, nextState) {
    return !_.isEmpty(nextState.charts) && !_.isEmpty(nextState.dashboards)
  },

  render: function () {
    let dashboards = this.state.dashboards
    if (!_.isUndefined(dashboards) && dashboards.length > 14) {
      dashboards = _.slice(dashboards, 0, 14)
    }

    const custom_dashboards = dashboards.map(dashboard => {
      if (!dashboard.builtin) {
        return (
          <NavMenuItem key={dashboard.id} href={'/dashboards/' + dashboard.id}>
            {dashboard.title}
          </NavMenuItem>
        )
      }
    })

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
      <NavMenuItem key={chart.id} href={'/charts/' + chart.id}>
        { chart.title }
      </NavMenuItem>
    )

    return (
      <ul className='dashboards-nav'>
        <li>
          <a href='/charts'>Charts</a>
          <ul className='dashboard-menu'>
            <li className='cta-menu-item'><a href='/charts/create'>Create a Chart</a></li>
            { custom_charts }
          </ul>
        </li>
        <li>
          <a href='/dashboards'>Dashboards</a>
          <ul className='dashboard-menu'>
            <li className='cta-menu-item'><a href='/dashboards/create'>Create a Dashboard</a></li>
            { custom_dashboards }
            <li className='separator'><hr /></li>
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
