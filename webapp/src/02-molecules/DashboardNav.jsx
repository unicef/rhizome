import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from '02-molecules/NavMenuItem.jsx'
import NavigationStore from 'stores/NavigationStore'
import ChartAPI from 'data/requests/Chart'

export default React.createClass({

  mixins: [
    Reflux.connect(NavigationStore),
    require('02-molecules/menus/MenuControl')
  ],

  componentWillMount () {
    ChartAPI.getCharts().then(response => {
      this.setState({customCharts: response})
    })
  },

  render: function () {
    var dashboards = this.state.dashboards
    var customDashboards = []
    var builtins = []

    if (!_.isUndefined(dashboards)) {
      if (dashboards.length > 14) {
        dashboards = _.slice(dashboards, 0, 14)
      }
    }

    _.forEach(dashboards, function(dashboard) {
      if (dashboard.builtin && dashboard.id !== -4 && dashboard.title.indexOf('Homepage') === -1) {
        builtins.push(
          <NavMenuItem key={dashboard.id} href={'/datapoints/dashboards/' +  _.kebabCase(dashboard.title)}>{dashboard.title}</NavMenuItem>
        )
      } else if (!dashboard.builtin)
        customDashboards.push(
          <NavMenuItem key={dashboard.id} href={'/datapoints/dashboards/' + dashboard.id}>{dashboard.title}</NavMenuItem>
        )
    }, this)

    let customCharts = this.state.customCharts.map(chart => {
      return <NavMenuItem key={chart.chart_json.id} href={'/datapoints/charts/' + chart.id}>{chart.chart_json.title}</NavMenuItem>
    })

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
