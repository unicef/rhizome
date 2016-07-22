import _ from 'lodash'
import moment from 'moment'
import React, { Component, PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';
import Placeholder from 'components/global/Placeholder'
import DateRangeSelect from 'components/select/DateRangeSelect'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import DropdownButton from 'components/button/DropdownButton'
import DropdownList from 'react-widgets/lib/DropdownList'

class CampaignDetail extends Component {

  constructor (props) {
    super(props)
    this.state = {}
  }

  componentDidMount() {
    if (!this.props.campaign_types.raw) {
      this.props.getAllCampaignTypes()
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.campaign.id !== this.state.id) {
      const campaign = Object.assign({}, nextProps.campaign)
      delete campaign.created_at
      this.setState(campaign)
    }
  }

  _updateParam = (param, value) => {
    const campaign = {}
    campaign[param] = value
    this.setState(campaign)
  }

  _saveCampaign = event => {
    event.preventDefault()
    this.props.updateCampaign(this.state)
  }

  render = () => {
    if (!this.state.id) {
      return <Placeholder height={300} />
    }
    const todays_date = moment().format('YYYY-MM-DD')
    const start_date = this.state.start_date ? moment(this.state.start_date).toDate() : todays_date
    const end_date = this.state.end_date ? moment(this.state.end_date).toDate() : todays_date
    const dateRangePicker = (
      <div className='date-range-picker'>
        <label htmlFor='campaign_type'>Dates: </label>
        <DateTimePicker
          text='Start date: '
          value={start_date}
          time={false}
          format={'YYYY-MM-DD'}
          onChange={date => this._updateParam('start_date', moment(date).format('YYYY-MM-DD'))} />
        <span>to</span>
        <DateTimePicker
          text='End date: '
          value={end_date}
          time={false}
          format={'YYYY-MM-DD'}
          onChange={date => this._updateParam('end_date', moment(date).format('YYYY-MM-DD'))} />
      </div>
    )

    const selected_location = this.state.top_lvl_location_id ? this.props.locations.index[this.state.top_lvl_location_id] : {name: 'Select Location'}
    const selected_indicator_tag = this.state.top_lvl_indicator_tag_id ? this.props.indicators.tag_index[this.state.top_lvl_indicator_tag_id] : {tag_name: 'Select Tag'}
    const selected_campaign_type = this.state.campaign_type_id ? this.props.campaign_types.index[this.state.campaign_type_id] : {name: 'Select Campaign Type'}

    return (
      <form className='medium-4 medium-centered columns resource-form' onSubmit={this._saveCampaign}>
        <h2>Campaign ID: {this.state.id}</h2>

        <label htmlFor='name'>Name: </label>
        <input
          type='text'
          defaultValue={this.state.name}
          onBlur={event => this._updateParam('name', event.target.value)}
        />

        <label>Top level location: </label>
        <DropdownButton
          style='full-width'
          items={this.props.locations.list || []}
          sendValue={id => this._updateParam('top_lvl_location_id', id)}
          item_plural_name='Locations'
          text={selected_location.name}
          icon='fa-globe'
          uniqueOnly/>

        <label>Top level indicator tag: </label>
        <DropdownButton
          style='full-width'
          items={_.toArray(this.props.indicators.tag_index)}
          sendValue={id => this._updateParam('top_lvl_indicator_tag_id', id)}
          title_field='tag_name'
          value_field='id'
          item_plural_name='Indicator Tags'
          text={selected_indicator_tag.tag_name}
          icon='fa-tag'/>

        <label>Campaign type: </label>
        <DropdownButton
          style='full-width'
          items={this.props.campaign_types.raw || []}
          sendValue={id => this._updateParam('campaign_type_id', id)}
          title_field='name'
          value_field='id'
          item_plural_name='Campaign Types'
          text={selected_campaign_type.name}
          icon='fa-tag'/>
        {dateRangePicker}
        <br />
        <button className='large primary button expand'>Save</button>
      </form>
    )
  }
}

export default CampaignDetail
