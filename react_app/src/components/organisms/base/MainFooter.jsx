import React from 'react'
import { Link } from 'react-router'

const styles = {
	position: 'fixed',
	bottom: 0,
	width: '100%',
	background: '#000000'
}

const MainFooter = () => (
  <footer className="row main-footer">
    <nav>
      <ul className="actions inline-list">
        <li><Link to="/manage_system/users"><i className="fa fa-cog"></i>Manage System</Link></li>
        <li><Link to="/react_app/source_data" ><i className="fa fa-plus"></i>Source Data</Link></li>
        <li><Link to="/react_app/enter_data" ><i className="fa fa-plus"></i>Enter Data</Link></li>
        <li><Link to="/react_app/charts">Charts</Link></li>
        <li><Link to="/react_app/dashboards">Dashboards</Link></li>
        <li><Link to="/react_app/campaigns">Campaigns</Link></li>
        <li><Link to="/react_app/indicators">Indicators</Link></li>
        <li><Link to="/react_app/locations">Locations</Link></li>
        <li><Link to="/react_app/users">Users</Link></li>
      </ul>
    </nav>
  </footer>
)

export default MainFooter