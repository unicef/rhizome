import React from 'react'
import CampaignDetailContainer from 'containers/CampaignDetailContainer'

const CampaignPage = ({params}) => (
  <div>
  	<h1>Campaign Page</h1>
		<CampaignDetailContainer campaign_id={params.campaign_id}/>
  </div>
)

export default CampaignPage