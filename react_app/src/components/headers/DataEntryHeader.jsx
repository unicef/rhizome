import _ from 'lodash'
import React from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'
import Placeholder from 'components/global/Placeholder'
import CampaignSelect from 'components/select/CampaignSelect'
import IndicatorTagSelect from 'components/select/IndicatorTagSelect'
import ResourceTable from 'components/molecules/ResourceTable'
import SwitchButton from 'components/form/SwitchButton'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import Moment from 'moment'
import momentLocalizer from 'react-widgets/lib/localizers/moment'
momentLocalizer(Moment)

const DataEntryHeader = props => {
  console.log('props', props)
  const formEntry = props.entry_type === 'campaign'

  const selected_indicator = _.isEmpty(props.selected_indicators) ? {name: 'Select Indicator'} : props.selected_indicators[0]
  const indicator_select = (
    <DropdownButton
      items={props.indicators.tree}
      item_plural_name='Indicators'
      text={selected_indicator.short_name || selected_indicator.name}
      sendValue={id => props.setGlobalIndicators(props.indicators.index[id])}
      style='dropdown-list'
      searchable
    />
  )

  const indicator_tag_select = (
    <IndicatorTagSelect
      indicator_tags={_.toArray(props.indicators.tag_index) || []}
      selected_indicator_tag={props.selected_indicator_tag}
      selectIndicatorTag={indicator_tag => {
        const indicators = indicator_tag.indicator_ids.map(id => props.indicators.index[id])
        props.setGlobalIndicatorTag(indicator_tag)
        props.setGlobalIndicators(indicators)
      }}
    />
  )

  const campaign_select = (
    <CampaignSelect
      campaigns={props.campaigns.raw || []}
      selected_campaign={props.selected_campaign}
      selectCampaign={props.selectGlobalCampaign}
    />
  )

  const location_select = (
    <DropdownButton
      items={props.locations.list}
      item_plural_name='Locations'
      text='Add Locations'
      style='button'
      searchable
      uniqueOnly
      sendValue={id => props.selectGlobalLocation(props.locations.index[id])}
    />
  )

  const date_select = (
    <DateTimePicker
      defaultValue={new Date()}
    />
  )

  const switch_button = (
    <SwitchButton
      name='entry_type'
      title='entry_type'
      id='entry_type'
      checked={!formEntry}
      onChange={props.toggleEntryType}
    />
  )

  return (
    <header className='row page-header'>
      <div className='medium-5 columns medium-text-left small-text-center'>
        <h1>Enter Data</h1>
      </div>
      <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
        <div className='page-header-filters'>
          { switch_button }
          { formEntry ? indicator_tag_select : indicator_select }
          { formEntry ? campaign_select : date_select }
          { location_select }
        </div>
      </div>
    </header>
  )
}

export default DataEntryHeader
