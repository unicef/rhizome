import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from '02-molecules/NavMenuItem.jsx'
import NavigationStore from 'stores/NavigationStore'
import ChartAPI from 'data/requests/ChartAPI'

let DashboadrNav = React.createClass({

  mixins: [
    Reflux.connect(NavigationStore),
    require('02-molecules/menus/MenuControl')
  ],

  componentWillMount () {
    ChartAPI.getCharts().then(response => {
      this.setState({ custom_charts: response })
    })
  },

  render: function () {
    let dashboards = this.state.dashboards
    let custom_dashboards = []
    let premade_dashboards = []

    if (!_.isUndefined(dashboards)) {
      if (dashboards.length > 14) {
        dashboards = _.slice(dashboards, 0, 14)
      }
    }

    // Dashboard Menu Items
    // ---------------------------------------------------------------------------
    _.forEach(dashboards, function (dashboard) {
      if (dashboard.builtin && dashboard.id !== -4 && dashboard.title.indexOf('Homepage') === -1) {
        premade_dashboards.push(
          <NavMenuItem key={dashboard.id} href={'/datapoints/dashboards/' +  _.kebabCase(dashboard.title)}>
            {dashboard.title}
          </NavMenuItem>)
      } else if (!dashboard.builtin) {
        custom_dashboards.push(
          <NavMenuItem key={dashboard.id} href={'/datapoints/dashboards/' + dashboard.id}>
            {dashboard.title}
          </NavMenuItem>)
      }
    }, this)

    // Chart Menu Items
    // ---------------------------------------------------------------------------
    let custom_charts = this.state.custom_charts.map(chart => {
      return <NavMenuItem key={chart.chart_json.id} href={'/datapoints/charts/' + chart.id}>
        { chart.chart_json.title }
      </NavMenuItem>
    })

    // Chart Menu Items
    // ---------------------------------------------------------------------------
    return (
      <ul className='dashboards-nav'>
        <li>
          <a href='/datapoints/explore'>Data</a>
        </li>
        <li>
          <a href='/datapoints/charts/'>Charts</a>
          <ul className='dashboard-menu animated slideDown'>
            { premade_dashboards }
            <li className='separator'>
              <hr />
            </li>
            { custom_charts }
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

export default DashboadrNav
