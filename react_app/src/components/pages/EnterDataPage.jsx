import React, {Component} from 'react'
import Placeholder from 'components/global/Placeholder'
import DataEntryHeader from 'components/headers/DataEntryHeader'
import EnterDataTable from 'components/organisms/enter_data/EnterDataTable'

class EnterDataPage extends Component {

  componentWillReceiveProps (nextProps) {
    if (nextProps.dataParamsChanged) {
      const query = {
        start_date: nextProps.start_date,
        end_date: nextProps.end_date,
        campaign__in: nextProps.selected_campaign.id,
        indicator_ids: nextProps.selected_indicators.map(indicator => indicator.id),
        location_ids: nextProps.selected_locations.map(location => location.id),
        depth_level: nextProps.depth_level || 0,
        data_type: nextProps.data_type,
        show_missing_data: 1
      }
      nextProps.getDatapoints(query)
    }
  }

  render () {
    const props = this.props
    const formEntry = props.data_type === 'campaign'
    const datapoints = props.datapoints.flattened
    const no_location = props.selected_locations.length <= 0
    const no_indicator = props.selected_indicators.length <= 0
    const placeholder_text = !formEntry ? 'an indicator' : 'a form'
    const placeholder = (
      <div>
        { no_location ? <Placeholder height={150} text={'Add location(s) to begin'} loading={false}/> : null }
        { no_indicator ? <Placeholder height={150} text={`Select ${placeholder_text} to begin`} loading={false}/> : null }
      </div>
    )

    return (
      <div className='data-entry-page'>
        <DataEntryHeader {...props} />
        <h2 className='subheader'>
          { !formEntry && props.selected_indicators[0] ? props.selected_indicators[0].name : '' }
        </h2>
        <div className='row'>
          <div className='medium-12 columns'>
            { datapoints ? <EnterDataTable {...props} /> : placeholder }
          </div>
        </div>
      </div>
    )
  }
}

export default EnterDataPage
