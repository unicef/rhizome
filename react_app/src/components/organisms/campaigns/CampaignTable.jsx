import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'

const columnDefs = [
  {headerName: "ID", field: "id"},
  {headerName: 'Name', field: 'name'},
  {headerName: 'Start_date', field: 'start_date'},
  {headerName: 'End_date', field: 'end_date'},
  {headerName: 'Office_id', field: 'office_id', hide: true},
  {headerName: 'Campaign_type_id', field: 'campaign_type_id', hide: true},
  {headerName: 'Pct_complete', field: 'pct_complete', hide: true},
  {headerName: 'Top_lvl_location_id', field: 'top_lvl_location_id', hide: true}
]

const CampaignTable = ({ campaigns, fetchCampaigns }) => (
  <ResourceTable
    rowData={_.toArray(campaigns)}
    onRefreshData={fetchCampaigns}
    columnDefs={columnDefs}
    resourcePath='campaigns' />
)

CampaignTable.propTypes = {
  campaigns: PropTypes.objectOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string,
    start_date: PropTypes.string,
    end_date: PropTypes.string,
    office_id: PropTypes.number,
    campaign_type_id: PropTypes.number,
    pct_complete: PropTypes.number,
    top_lvl_location_id: PropTypes.number
  }).isRequired)
}

export default CampaignTable