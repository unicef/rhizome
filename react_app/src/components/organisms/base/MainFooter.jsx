import React from 'react'
import { Link } from 'react-router'

const styles = {
	position: 'fixed',
	bottom: 0,
	width: '100%',
	background: '#000000'
}

const MainFooter = () => (
  <footer style={styles}>
  	<nav>
  		<ul className='inline-list'>
  			<li><Link to='/manage_system'>Manage System</Link></li>
  			<li><Link to='/enter_data'>Enter Data</Link></li>
  			<li><Link to='/source_data'>View Source Data</Link></li>
  		</ul>
  		<ul className='inline-list'>
  			<li><Link to='/about'>About</Link></li>
  			<li><Link to='/sitemap'>Sitemap</Link></li>
  			<li><Link to='/bug_report'>Report a Bug</Link></li>
  			<li><Link to='/contact'>Contact Us</Link></li>
  		</ul>
  	</nav>
  </footer>
)

export default MainFooter