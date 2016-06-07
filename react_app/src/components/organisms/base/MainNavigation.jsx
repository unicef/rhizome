import React, { Component } from 'react'
import { Link } from 'react-router'

export default class MainNavigation extends Component {
  render () {
  	return (
      <nav className='top-bar'>
        <ul className='dashboards-nav'>
          <li>
            <a href='/charts'>Charts</a>
            <ul className='dashboard-menu'>
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

