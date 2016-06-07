import _ from 'lodash'
import React, { Component } from 'react'
import { Link } from 'react-router'

class MainNavigation extends Component {
  render () {
    let charts = _.sortBy(this.props.charts, 'title')
    if (!_.isUndefined(charts) && charts.length > 10) {
      charts = _.slice(charts, 0, 10)
    }
    const custom_charts = charts.map(chart =>
      <li key={chart.id}>
        <a role='menuitem' href={'/charts/' + chart.id}>{chart.title}</a>
      </li>
    )

  	return (
      <nav className='top-bar'>
        <ul className='dashboards-nav'>
          <li>
            <a href='/charts'>Charts</a>
            <ul className='dashboard-menu'>
              {custom_charts}
              <li className='separator'><hr />
                <a href='/charts'>See All Charts</a>
              </li>
            </ul>
          </li>
          <li>
            <a href='/dashboards'>Dashboards</a>
            <ul className='dashboard-menu'>
            </ul>
          </li>
          <li className='log-out'>
            <a href='/accounts/logout?next=/' title='logout'>
              Log Out &nbsp;
              <i className='fa fa-lg fa-sign-out'/>
            </a>
          </li>
        </ul>
      </nav>
  	)
  }
}

export default MainNavigation