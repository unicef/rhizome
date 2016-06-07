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
        <li><a href="/manage_system/users"><i className="fa fa-cog"></i>Manage System</a></li>
        <li><a href="/source-data" ><i className="fa fa-file"></i>Source Data</a></li>
        <li><a href="/react_app/enter_data" ><i className="fa fa-plus"></i>Enter Data</a></li>
      </ul>
    </nav>
  </footer>
)

export default MainFooter