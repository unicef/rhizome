import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchCampaigns = createAction(
	'FETCH_CAMPAIGNS', () => RhizomeAPI.get('campaign/')
)
export const fetchCampaignsFailure = createAction('FETCH_CAMPAIGNS_FAILURE')
export const fetchCampaignsSuccess = createAction('FETCH_CAMPAIGNS_SUCCESS')

