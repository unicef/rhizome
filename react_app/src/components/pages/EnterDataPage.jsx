import _ from 'lodash'
import React, {Component} from 'react'
import {Multiselect} from 'react-widgets'
import DropdownButton from 'components/button/DropdownButton'
import Placeholder from 'components/global/Placeholder'
import CampaignSelect from 'components/select/CampaignSelect'
import IndicatorTagSelect from 'components/select/IndicatorTagSelect'

const selectLocation = () => {
  console.log('hello')
}


class EnterDataPage extends Component {

  // componentWillReceiveProps(nextProps) {
  //   if (nextProps.selected_campaign && nextProps.selected_locations.length > 0 && nextProps.selected_indicators.length > 0) {
  //     const query = {
  //       campaign__in: nextProps.selected_campaign.id,
  //       indicator_ids: nextProps.selected_indicators.map(indicator => indicator.id),
  //       location_ids: nextProps.selected_locations.map(location => location.id),
  //       show_missing_data: 1,
  //       source_name: ''
  //     }
  //     nextProps.fetchDatapoints(query)
  //   }
  // }


  // componentWillReceiveProps(nextProps) {
  //   if (nextProps.selected_campaign && nextProps.selected_locations.length > 0 && nextProps.selected_indicators.length > 0) {
  //     const query = {
  //       campaign__in: nextProps.selected_campaign.id,
  //       indicator_ids: nextProps.selected_indicators.map(indicator => indicator.id),
  //       location_ids: nextProps.selected_locations.map(location => location.id),
  //       show_missing_data: 1,
  //       source_name: ''
  //     }
  //     nextProps.fetchDatapoints(query)
  //   }
  // }

  render () {
    console.log('this.props.datapoints', this.props.datapoints)
    const props = this.props
    const datapoints = [] // temporary

    const campaign_select = (
      <CampaignSelect
        campaigns={props.campaigns.raw || []}
        selected_campaign={props.selected_campaign}
        selectCampaign={() => {
          props.selectGlobalCampaign()
        }}
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
        sendValue={id => {
          props.selectGlobalLocation(props.locations.index[id])
        }}
      />
    )

    const placeholder = !props.selected_locations
      ? <Placeholder height={300} text={'Add location(s) to begin'} loading={false}/>
      : <Placeholder height={300}/>

    return (
      <div>
        <header className='row page-header'>
          <div className='medium-5 columns medium-text-left small-text-center'>
            <h1>Enter Data</h1>
          </div>
          <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
            <div className='page-header-filters'>
              { indicator_tag_select }
              { campaign_select }
              { location_select }
            </div>
          </div>
        </header>
        <div className='row'>
          <div className='medium-12 columns'>
            { datapoints.flattened ? data_table : placeholder }
          </div>
        </div>
      </div>
    )
  }
}

export default EnterDataPage
