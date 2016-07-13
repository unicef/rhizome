import React, {Component} from 'react'
import Placeholder from 'components/global/Placeholder'
import DataEntryHeader from 'components/headers/DataEntryHeader'
import CampaignDataEntryTable from 'components/organisms/enter_data/CampaignDataEntryTable'
import DateDataEntryTable from 'components/organisms/enter_data/DateDataEntryTable'

class DataEntryPage extends Component {

  componentWillReceiveProps (nextProps) {
    if (nextProps.data_type !== nextProps.params.data_type) {
      this.props.toggleEntryType()
    }
    if (nextProps.dataParamsChanged) {
      nextProps.getDatapoints(nextProps)
    }
  }

  render () {
    const props = this.props
    const formEntry = props.data_type === 'campaign'
    const datapoints = props.datapoints.flattened
    const no_location = props.selected_locations.length <= 0
    const no_indicator = props.selected_indicators.length <= 0
    const indicator_text = !formEntry ? 'an indicator' : 'a form'
    const location_text = !formEntry ? 'locations' : 'a location'
    const full_text = () => {
      if (no_indicator && no_location) {
        return `Select ${indicator_text} and ${location_text} to begin`
      } else if (no_indicator && !no_location) {
        return `Select ${indicator_text} to begin`
      } else if (!no_indicator && no_location) {
        return `Select ${location_text} to begin`
      }
    }
    const placeholder = no_location || no_indicator ? (
       <Placeholder height={300} text={full_text()} loading={false}/>
    ) : <Placeholder height={300} />

    const data_table = formEntry ? <CampaignDataEntryTable {...props} /> : <DateDataEntryTable {...props}/>


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

export default DataEntryPage
