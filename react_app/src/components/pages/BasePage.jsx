import React, { Component } from 'react'
import NProgress from 'react-nprogress'

import MainFooter from 'components/organisms/base/MainFooter'
import MainHeader from 'components/organisms/base/MainHeader'

export default class BasePage extends Component {

	componentWillMount() {
		this.props.getInitialData()
	}

  componentWillUpdate (nextProps, nextState) {
		NProgress.start()
  }

  componentDidUpdate (nextProps, nextState) {
		NProgress.done()
  }

  render () {
  	return (
			<div >
				<MainHeader charts={this.props.charts} dashboards={this.props.dashboards} />
			  <main role='main' className="row">{this.props.children}</main>
				<MainFooter />
			</div>
  	)
  }
}
