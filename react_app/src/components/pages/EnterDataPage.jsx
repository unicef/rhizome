import _ from 'lodash'
import React, {Component} from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'
import Placeholder from 'components/global/Placeholder'
import DataEntryHeader from 'components/headers/DataEntryHeader'
import CampaignSelect from 'components/select/CampaignSelect'
import IndicatorTagSelect from 'components/select/IndicatorTagSelect'
import ResourceTable from 'components/molecules/ResourceTable'
import SwitchButton from 'components/form/SwitchButton'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import Moment from 'moment'
import momentLocalizer from 'react-widgets/lib/localizers/moment'
momentLocalizer(Moment)

class EnterDataPage extends Component {

  componentWillReceiveProps(nextProps) {
    if (nextProps.dataParamsChanged) {
      const query = {
        campaign__in: nextProps.selected_campaign.id,
        indicator_ids: nextProps.selected_indicators.map(indicator => indicator.id),
        location_ids: nextProps.selected_locations.map(location => location.id),
        depth_level: nextProps.depth_level || 0,
        time_grouping: 'campaign',
        show_missing_data: 1,
        source_name: ''
      }
      nextProps.getDatapoints(query)
    }
  }

  render () {
    const props = this.props
    const formEntry = props.entry_type === 'campaign'

    const no_location = props.selected_locations.length <= 0
    const no_indicator = props.selected_indicators.length <= 0
    const placeholder_text = !formEntry ? 'an indicator' : 'a form'
    const placeholder = (
      <div>
        { no_location ? <Placeholder height={150} text={'Add location(s) to begin'} loading={false}/> : null }
        { no_indicator ? <Placeholder height={150} text={`Select ${placeholder_text} to begin`} loading={false}/> : null }
      </div>
    )
    const columnDefs = [
      {headerName: "ID", field: "id", suppressMenu: true},
      {headerName: "Campaign ID", field: "campaign_id", editable: true},
      {headerName: "Indicator ID", field: "indicator_id"},
      {headerName: "Location ID", field: "value"},
      {headerName: "Value", field: "value"}
    ]
    const raw_data_table = (
      <ResourceTable
        rowData={props.table_data.rows || []}
        columnDefs={props.table_data.columns}
        resourcePath='datapoints'
      />
    )

    return (
      <div className='data-entry-page'>
        <DataEntryHeader {...props} />
        <h2 className='subheader'>
          { !formEntry && props.selected_indicators[0] ? props.selected_indicators[0].name : '' }
        </h2>
        <div className='row'>
          <div className='medium-12 columns'>
            { props.datapoints.raw ? raw_data_table : placeholder }
          </div>
        </div>
      </div>
    )
  }
}

export default EnterDataPage
