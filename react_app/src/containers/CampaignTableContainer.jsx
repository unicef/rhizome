import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import CampaignTable from 'components/organisms/campaigns/CampaignTable'
import { fetchCampaigns } from 'actions/campaign_actions'

const mapStateToProps = (state) => ({ campaigns: state.campaigns })

const mapDispatchToProps = (dispatch) => bindActionCreators({fetchCampaigns}, dispatch)

const CampaignTableContainer = connect(mapStateToProps, mapDispatchToProps)(CampaignTable)

export default CampaignTableContainer
