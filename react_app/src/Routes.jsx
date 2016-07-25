import React from 'react'
import { Route } from 'react-router'

import BasePageContainer from 'containers/BasePageContainer'

import CampaignContainer from 'containers/CampaignContainer'
import CampaignsContainer from 'containers/CampaignsContainer'

import IndicatorContainer from 'containers/IndicatorContainer'
import IndicatorsContainer from 'containers/IndicatorsContainer'

import LocationContainer from 'containers/LocationContainer'
import LocationsContainer from 'containers/LocationsContainer'

import UserContainer from 'containers/UserContainer'
import UsersContainer from 'containers/UsersContainer'

import ChartsPage from 'components/pages/charts/ChartsPage'
import ChartPage from 'components/pages/charts/ChartPage'
import ChartEditPage from 'components/pages/charts/ChartEditPage'

import DashboardsPage from 'components/pages/dashboards/DashboardsPage'
import DashboardPage from 'components/pages/dashboards/DashboardPage'
import DashboardEditPage from 'components/pages/dashboards/DashboardEditPage'

import SourceDataPageContainer from 'containers/SourceDataPageContainer'
import DataEntryPageContainer from 'containers/DataEntryPageContainer'

import AboutPage from 'components/pages/info/AboutPage'
import BugReportPage from 'components/pages/info/BugReportPage'
import ContactPage from 'components/pages/info/ContactPage'
import SitemapPage from 'components/pages/info/SitemapPage'



const Routes = (
	<Route path="/react_app" component={BasePageContainer}>

		// RESOURCE ROUTES
		//---------------------------------------------------------
	  <Route path="/react_app/campaigns" component={CampaignsContainer}/>
	  <Route path="/react_app/campaigns/:campaign_id" component={CampaignContainer}/>

	  <Route path="/react_app/indicators" component={IndicatorsContainer}/>
	  <Route path="/react_app/indicators/:indicator_id" component={IndicatorContainer}/>

	  <Route path="/react_app/locations" component={LocationsContainer}/>
	  <Route path="/react_app/locations/:location_id" component={LocationContainer}/>

	  <Route path="/react_app/users" component={UsersContainer}/>
	  <Route path="/react_app/users/:user_id" component={UserContainer}/>

	  <Route path="/react_app/charts" component={ChartsPage}/>
	  <Route path="/react_app/charts/:chart_id" component={ChartPage}/>
	  <Route path="/react_app/charts/:chart_id/edit" component={ChartEditPage}/>

	  <Route path="/react_app/dashboards" component={DashboardsPage}/>
	  <Route path="/react_app/dashboards/:dashboard_id" component={DashboardPage}/>
	  <Route path="/react_app/dashboards/:dashboard_id/edit" component={DashboardEditPage}/>

		// INFO ROUTES
		//---------------------------------------------------------
	  <Route path="/react_app/about" component={AboutPage}/>
	  <Route path="/react_app/bug_report" component={BugReportPage}/>
	  <Route path="/react_app/contact" component={ContactPage}/>
	  <Route path="/react_app/sitemap" component={SitemapPage}/>

		// OTHER ROUTES
		//---------------------------------------------------------
	  <Route path="/react_app/source_data" component={SourceDataPageContainer}/>
	  <Route path="/react_app/enter_data(/:data_type)" component={DataEntryPageContainer}/>
	</Route>
)

export default Routes