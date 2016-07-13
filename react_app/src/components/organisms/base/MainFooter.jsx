import React from 'react'
import { Link } from 'react-router'

const styles = {
	position: 'fixed',
	bottom: 0,
	width: '100%',
	background: '#000000'
}

const active_link = {
  background: '#6B7A83'
}

const MainFooter = () => (
  <footer className="row main-footer">
    <nav>
      <ul className="actions left inline-list">
        <li><Link to="/react_app/source_data" activeStyle={active_link}><i className="fa fa-plus"></i>Upload Data</Link></li>
        <li><Link to="/react_app/enter_data/campaign" params={{data_type: 'campaign'}} activeStyle={active_link}><i className="fa fa-plus"></i>Form Entry</Link></li>
        <li><Link to="/react_app/enter_data/date" activeStyle={active_link}><i className="fa fa-plus"></i>Date Entry</Link></li>
      </ul>
      <ul className="actions right inline-list">
        <li><Link to="/react_app/campaigns" activeStyle={active_link}><i className="fa fa-calendar"></i>Campaigns</Link></li>
        <li><Link to="/react_app/indicators" activeStyle={active_link}><i className="fa fa-tachometer"></i>Indicators</Link></li>
        <li><Link to="/react_app/locations" activeStyle={active_link}><i className="fa fa-globe"></i>Locations</Link></li>
        <li><Link to="/react_app/users" activeStyle={active_link}><i className="fa fa-users"></i>Users</Link></li>
      </ul>
    </nav>
  </footer>
)

export default MainFooter