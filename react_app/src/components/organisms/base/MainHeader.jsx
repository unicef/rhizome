import React, { Component } from 'react'
import MainNavigation from 'components/organisms/base/MainNavigation'

export default class MainHeader extends Component {
  render () {
  	return (
		  <header className="no-print">
		    <div className="row navigation-bar">
		      <a href="/" className="logo">
		        <img className="image-style" src="/static/img/RhizomeAfghanEOC.jpg" />
		      </a>
		      <nav className="dashboard-control">
		        <div id="dashboards-nav">
		        	<MainNavigation charts={this.props.charts} />
		        </div>
		      </nav>
		    </div>
		  </header>
  	)
  }
}