import React, { Component } from 'react'
import { Link } from 'react-router'

export default class MainNavigation extends Component {
  render () {
  	return (
      <nav className='top-bar'>
        <div className='top-bar-left'>
          <ul className='menu'>
            <li className='menu-text'><Link to={'/'}>Rhizome</Link></li>
            <li><Link to={'/users'}>Users</Link></li>
            <li><Link to={'/indicators'}>Indicators</Link></li>
            <li><Link to={'/locations'}>Locations</Link></li>
            <li><Link to={'/campaigns'}>Campaigns</Link></li>
            <li><Link to={'/charts'}>Charts</Link></li>
          </ul>
        </div>
      </nav>
  	)
  }
}