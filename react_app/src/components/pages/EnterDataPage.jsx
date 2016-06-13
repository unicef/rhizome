import _ from 'lodash'
import React, {Component} from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'
import Placeholder from 'components/global/Placeholder'
import CampaignSelect from 'components/select/CampaignSelect'
import IndicatorTagSelect from 'components/select/IndicatorTagSelect'
import ResourceTable from 'components/molecules/ResourceTable'

class EnterDataPage extends Component {

  componentWillReceiveProps(nextProps) {
    if (nextProps.dataParamsChanged) {
      const query = {
        campaign__in: nextProps.selected_campaign.id,
        indicator_ids: nextProps.selected_indicators.map(indicator => indicator.id),
        location_ids: nextProps.selected_locations.map(location => location.id),
        time_grouping: 'campaign',
        show_missing_data: 1,
        source_name: ''
      }
      nextProps.getDatapoints(query)
    }
  }

  render () {
    const props = this.props

    const campaign_select = (
      <CampaignSelect
        campaigns={props.campaigns.raw || []}
        selected_campaign={props.selected_campaign}
        selectCampaign={props.selectGlobalCampaign}
      />
    )

    const selected_indicator = _.isEmpty(props.selected_indicators) ? {name: 'Select Indicator'} : this.props.selected_indicators[0]
    const indicator_select = (
      <DropdownButton
        items={props.indicators.tree}
        item_plural_name='Indicators'
        style='dropdown-list'
        searchable
        text={selected_indicator.short_name || selected_indicator.name}
        sendValue={id => props.setGlobalIndicators(props.indicators.index[id])}
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
    const location_select  = (
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

    const placeholder = !props.selected_locations
      ? <Placeholder height={300} text={'Add location(s) to begin'} loading={false}/>
      : <Placeholder height={300}/>

    const columnDefs = [
      {headerName: "ID", field: "id", suppressMenu: true},
      {headerName: "Campaign ID", field: "campaign_id", editable: true},
      {headerName: "Indicator ID", field: "indicator_id"},
      {headerName: "Location ID", field: "location_id"},
      {headerName: "Value", field: "value"}
    ]

    const data_table = (
      <ResourceTable
        rowData={props.datapoints.raw || []}
        columnDefs={columnDefs}
        resourcePath='datapoints'
      />
    )

    return (
      <div>
        <header className='row page-header'>
          <div className='medium-5 columns medium-text-left small-text-center'>
            <h1>Enter Data</h1>
          </div>
          <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
            <div className='page-header-filters'>
              { indicator_select }
              { indicator_tag_select }
              { campaign_select }
              { location_select }
            </div>
          </div>
        </header>
        <div className='row'>
          <div className='medium-12 columns'>
            { props.datapoints.raw ? data_table : placeholder }
          </div>
        </div>
      </div>
    )
  }
}

export default EnterDataPage
