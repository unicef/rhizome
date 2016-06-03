import React from 'react'
import { Route } from 'react-router'

import BasePageContainer from 'containers/BasePageContainer'

import CampaignsPage from 'components/pages/campaigns/CampaignsPage'
import CampaignPage from 'components/pages/campaigns/CampaignPage'
import CampaignEditPage from 'components/pages/campaigns/CampaignEditPage'

import ChartsPage from 'components/pages/charts/ChartsPage'
import ChartPage from 'components/pages/charts/ChartPage'
import ChartEditPage from 'components/pages/charts/ChartEditPage'

import IndicatorsPage from 'components/pages/indicators/IndicatorsPage'
import IndicatorPage from 'components/pages/indicators/IndicatorPage'
import IndicatorEditPage from 'components/pages/indicators/IndicatorEditPage'

import LocationsPage from 'components/pages/locations/LocationsPage'
import LocationPage from 'components/pages/locations/LocationPage'
import LocationEditPage from 'components/pages/locations/LocationEditPage'

import SourceDatasPage from 'components/pages/source_data/SourceDatasPage'
import SourceDataPage from 'components/pages/source_data/SourceDataPage'
import SourceDataEditPage from 'components/pages/source_data/SourceDataEditPage'

import UsersPage from 'components/pages/users/UsersPage'
import UserPage from 'components/pages/users/UserPage'
import UserEditPage from 'components/pages/users/UserEditPage'

import AboutPage from 'components/pages/info/AboutPage'
import BugReportPage from 'components/pages/info/BugReportPage'
import ContactPage from 'components/pages/info/ContactPage'
import SitemapPage from 'components/pages/info/SitemapPage'

import EnterDataPage from 'components/pages/EnterDataPage'
import ManageSystemPage from 'components/pages/ManageSystemPage'

const Routes = (
	<Route path="/" component={BasePageContainer}>

		// RESOURCE ROUTES
		//---------------------------------------------------------
	  <Route path="/campaigns" component={CampaignsPage}/>
	  <Route path="/campaigns/:campaign_id" component={CampaignPage}/>
	  <Route path="/campaigns/:campaign_id/edit" component={CampaignEditPage}/>

	  <Route path="/new_charts" component={ChartsPage}/>
	  <Route path="/new_charts/:chart_id" component={ChartPage}/>
	  <Route path="/new_charts/:chart_id/edit" component={ChartEditPage}/>

	  <Route path="/indicators" component={IndicatorsPage}/>
	  <Route path="/indicators/:indicator_id" component={IndicatorPage}/>
	  <Route path="/indicators/:indicator_id/edit" component={IndicatorEditPage}/>

	  <Route path="/locations" component={LocationsPage}/>
	  <Route path="/locations/:location_id" component={LocationPage}/>
	  <Route path="/locations/:location_id/edit" component={LocationEditPage}/>

	  <Route path="/source_data" component={SourceDatasPage}/>
	  <Route path="/source_data/:source_data_id" component={SourceDataPage}/>
	  <Route path="/source_data/:source_data_id/edit" component={SourceDataEditPage}/>

	  <Route path="/users" component={UsersPage}/>
	  <Route path="/users/:user_id" component={UserPage}/>
	  <Route path="/users/:user_id/edit" component={UserEditPage}/>

		// INFO ROUTES
		//---------------------------------------------------------
	  <Route path="/about" component={AboutPage}/>
	  <Route path="/bug_report" component={BugReportPage}/>
	  <Route path="/contact" component={ContactPage}/>
	  <Route path="/sitemap" component={SitemapPage}/>

		// OTHER ROUTES
		//---------------------------------------------------------
	  <Route path="/enter_data" component={EnterDataPage}/>
	  <Route path="/manage_system" component={ManageSystemPage}/>
	</Route>
)

export default Routes