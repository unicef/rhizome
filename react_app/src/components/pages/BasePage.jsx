import React, { Component } from 'react'
import NProgress from 'react-nprogress'

import MainFooter from 'components/organisms/base/MainFooter'
import MainNavigation from 'components/organisms/base/MainNavigation'
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
				<MainNavigation />
				<MainHeader />
				  <div className="row">
						{ this.props.children }
					</div>
				<MainFooter />
			</div>
  	)
  }
}
