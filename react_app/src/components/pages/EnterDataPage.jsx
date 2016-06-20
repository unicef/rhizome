import React, {Component} from 'react'
import Placeholder from 'components/global/Placeholder'
import DataEntryHeader from 'components/headers/DataEntryHeader'
import EnterDataTable from 'components/organisms/enter_data/EnterDataTable'

class EnterDataPage extends Component {

  componentWillReceiveProps (nextProps) {
    if (nextProps.dataParamsChanged) {
      const query = {
        indicator_ids: nextProps.selected_indicators.map(indicator => indicator.id),
        location_ids: nextProps.selected_locations.map(location => location.id),
        location_depth: nextProps.location_depth || 1,
        data_type: nextProps.data_type,
        show_missing_data: 1
      }
      if (nextProps.data_type === 'campaign' && nextProps.selected_campaign) {
        query.campaign__in = nextProps.selected_campaign.id
      } else {
        query.start_date = nextProps.start_date,
        query.end_date = nextProps.end_date
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
    const placeholder = no_location || no_indicator ? (
      <div>
        { no_location ? <Placeholder height={150} text={'Add location(s) to begin'} loading={false}/> : null }
        { no_indicator ? <Placeholder height={150} text={`Select ${placeholder_text} to begin`} loading={false}/> : null }
      </div>
    ) : <Placeholder height={300} />

    const data_table = <EnterDataTable {...props} />

    return (
      <div className='data-entry-page'>
        <DataEntryHeader {...props} />
        <div className='row'>
          <div className='medium-12 columns'>
            { datapoints ? data_table : placeholder }
          </div>
        </div>
      </div>
    )
  }
}

export default EnterDataPage
