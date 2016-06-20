import _ from 'lodash'
import moment from 'moment'
import React from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'
import CampaignSelect from 'components/select/CampaignSelect'
import IndicatorTagSelect from 'components/select/IndicatorTagSelect'
import SwitchButton from 'components/form/SwitchButton'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import DateRangeSelect from 'components/select/DateRangeSelect'
import momentLocalizer from 'react-widgets/lib/localizers/moment'
momentLocalizer(moment)

const DataEntryHeader = props => {
  const formEntry = props.data_type === 'campaign'

  const selected_indicator = _.isEmpty(props.selected_indicators) ? {name: 'Select Indicator'} : props.selected_indicators[0]
  const indicator_select = (
    <DropdownButton
      items={props.indicators.tree}
      icon='fa-chevron-down'
      item_plural_name='Indicators'
      text={selected_indicator.name || selected_indicator.short_name}
      sendValue={id => props.setGlobalIndicators(props.indicators.index[id])}
      style='dropdown-list'
      searchable
    />
  )

  const indicator_tag_select = (
    <DropdownButton
      items={_.toArray(props.indicators.tag_index) || []}
      item_plural_name='Forms'
      icon='fa-chevron-down'
      text={props.selected_indicator_tag ? props.selected_indicator_tag.tag_name : 'Select Form'}
      value_field='id'
      title_field='tag_name'
      sendValue={id => {
        const indicator_tag = props.indicators.tag_index[id]
        const indicators = indicator_tag.indicator_ids.map(id => props.indicators.index[id])
        props.setGlobalIndicatorTag(indicator_tag)
        props.setGlobalIndicators(indicators)
      }}
      style='dropdown-list'
      searchable
    />
  )

  const campaign_select = (
    <DropdownButton
      items={props.campaigns.raw || []}
      item_plural_name='Campaigns'
      value_field='id'
      title_field='name'
      icon='fa-chevron-down'
      text={props.selected_campaign ? props.selected_campaign.name : 'Select Campaign'}
      style='dropdown-list'
      sendValue={id => props.selectGlobalCampaign(props.campaigns.index[id])}
    />
  )

  const location_select = (
    <DropdownButton
      items={props.locations.list}
      item_plural_name='Locations'
      text='Select Location'
      style='button select-location-button'
      searchable
      uniqueOnly
      sendValue={id => props.setGlobalLocations(props.locations.index[id])}
    />
  )

  const start_date = moment(props.start_date).toDate()
  const end_date = moment(props.end_date).toDate()
  const date_select = (
    <div className='date-range-picker'>
      <DateTimePicker
        value={start_date}
        time={false}
        format={'YYYY-MM-DD'}
        onChange={date => props.setDataEntryStartDate(moment(date).format('YYYY-MM-DD'))} />
      <span>to</span>
      <DateTimePicker
        value={end_date}
        time={false}
        format={'YYYY-MM-DD'}
        onChange={date => props.setDataEntryEndDate(moment(date).format('YYYY-MM-DD'))} />
    </div>
  )

  const switch_button = (
    <SwitchButton
      name='data_type'
      title='data_type'
      id='data_type'
      checked={!formEntry}
      onChange={props.toggleEntryType}
    />
  )

  const getChildrenLocations = (parent_location) => {
    let children_locations = props.locations.raw.filter(location => location.parent_location_id === parent_location.id)
    children_locations.unshift(parent_location)
    return children_locations
  }

  const location_depth_toggle = (
    <input
      type='checkbox'
      checked={props.location_depth}
      onChange={() => {
        const new_location_depth = props.location_depth === 1 ? 0 : 1
        props.setGlobalLocationDepth(new_location_depth)
        const selected_location = props.selected_locations[0]
        const new_locations = new_location_depth === 0 ? selected_location : getChildrenLocations(selected_location)
        props.setGlobalLocations(new_locations)
      }}
    />
  )

  return (
    <header className='row page-header'>
      <div className='medium-12 columns medium-text-left small-text-center'>
        <h1>Enter {props.data_type} Data
          { switch_button }
        </h1>
      </div>
      <div className='medium-7 columns medium-text-left small-text-center dashboard-actions'>
        { formEntry ? indicator_tag_select : indicator_select }
      </div>
      <div className='medium-5 columns medium-text-right small-text-center dashboard-actions'>
        { formEntry ? campaign_select : date_select }
        { location_select }
      </div>
    </header>
  )
}

export default DataEntryHeader
