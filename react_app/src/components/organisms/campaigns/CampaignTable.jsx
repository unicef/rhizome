import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

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

const CampaignTable = ({campaigns, getAllCampaigns}) => {
  return campaigns.raw ? (
    <ResourceTable
      rowData={campaigns.raw}
      onRefreshData={() => getAllCampaigns()}
      columnDefs={columnDefs}
      resourcePath='campaigns' />
    ) : <Placeholder />
}

export default CampaignTable