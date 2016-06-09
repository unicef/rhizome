import _ from 'lodash'
import React, { Component } from 'react'
import { Link } from 'react-router'

class MainNavigation extends Component {
  render () {
    let dashboards = this.props.dashboards.raw
    if (dashboards && dashboards.length > 14) {
      dashboards = _.slice(dashboards, 0, 14)
    }
    const custom_dashboards = dashboards ? dashboards.map(dashboard =>
      <li key={dashboard.id}>
        <a role='menuitem' href={'/dashboards/' + dashboard.id}>{dashboard.title}</a>
      </li>
    ) : <li>Loading ...</li>

    let charts = _.sortBy(this.props.charts.raw, 'title')
    if (charts && charts.length > 10) {
      charts = _.slice(charts, 0, 10)
    }
    const custom_charts = charts ? charts.map(chart =>
      <li key={chart.id}>
        <a role='menuitem' href={'/charts/' + chart.id}>{chart.title}</a>
      </li>
    ) : <li>Loading ...</li>

    const create_chart_button = this.props.superuser ? (
      <li className='cta-menu-item'><a href='/charts/create'>Create a Chart</a></li>
    ) : null

    const create_dashboard_button = this.props.superuser ? (
      <li className='cta-menu-item'><a href='/dashboards/create'>Create a Dashboard</a></li>
    ) : null

  	return (
      <nav className='top-bar'>
        <ul className='dashboards-nav'>
          <li>
            <a href='/charts'>Charts</a>
            <ul className='dashboard-menu'>
              { create_chart_button }
              { custom_charts }
              <li className='separator'><hr />
                <a href='/charts'>See All Charts</a>
              </li>
            </ul>
          </li>
          <li>
            <a href='/dashboards'>Dashboards</a>
            <ul className='dashboard-menu'>
              { custom_dashboards }
              { create_dashboard_button }
            </ul>
          </li>
          <li className='log-out'>
            <a href='/accounts/logout?next=/' title='logout'>
              Log Out &nbsp;<i className='fa fa-lg fa-sign-out'/>
            </a>
          </li>
        </ul>
      </nav>
  	)
  }
}

export default MainNavigation