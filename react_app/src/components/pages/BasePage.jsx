import React, { Component } from 'react'
import NProgress from 'react-nprogress'

import MainFooter from 'components/organisms/base/MainFooter'
import MainHeader from 'components/organisms/base/MainHeader'

export default class BasePage extends Component {

	componentWillMount() {
		this.props.fetchAllMeta()
	}

  componentWillUpdate (nextProps, nextState) {
		NProgress.start()
  }

  render () {
  	return (
			<div role='main'>
				<MainHeader charts={this.props.charts} />
			  <div className="row">{this.props.children}</div>
				<MainFooter />
			</div>
  	)
  }
}
