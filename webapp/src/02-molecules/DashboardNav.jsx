import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavMenuItem from '02-molecules/NavMenuItem.jsx'
import NavigationStore from 'stores/NavigationStore'
import ChartAPI from 'data/requests/ChartAPI'

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
        <li className='medium-4 columns'>
          <a href='/datapoints/explore'>Explore Data</a>
        </li>
        <li className='medium-4 columns'>
          <a href='/datapoints/charts/'>View Charts</a>
          <ul className='dashboard-menu'>
            {builtins}
            <li className='separator'>
              <hr />
            </li>
            {customCharts}
          </ul>
        </li>
        <li className='medium-4 columns log-out'>
          <a href='/accounts/logout?next=/' title='logout'>
          log out &nbsp;
            <i className='fa fa-lg fa-sign-out'/>
          </a>
        </li>
      </ul>
    )
  }
})
