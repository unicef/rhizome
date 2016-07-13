import moment from 'moment'
import React, { Component, PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';
import Placeholder from 'components/global/Placeholder'
import DateMultiSelect from 'components/select/DateRangeSelect'
import DropdownButton from 'components/button/DropdownButton'

  // _setOffice: function (event) {
  //   CampaignPageActions.setOffice(event.target.value)
  // },
  // _setCampaignName: function (event) {
  //   CampaignPageActions.setCampaignName(event.target.value)
  // },
  // _setIndicatorTag: function (tagId) {
  //   CampaignPageActions.setIndicatorTag(tagId)
  // },
  // _setCampaignType: function (event) {
  //   CampaignPageActions.setCampaignType(event.target.value)
  // },
  // _save: function (e) {
  //   e.preventDefault()
  //   this.state.postData.name = this.refs.campaignName.getDOMNode().value
  //   this.state.postData.start_date = moment(this.state.campaign.start).format('YYYY-M-D')
  //   this.state.postData.end_date = moment(this.state.campaign.end).format('YYYY-M-D')
  //   CampaignPageActions.saveCampaign(this.state.postData)
  // },

class CampaignDetail extends Component {

  constructor (props) {
    super(props)
    console.log('props', props)
    this.state = {
      campaign_name: props.campaign.name,
    }
  }

  _setCampaignName = (event) => {
    this.setState({campaign_name: event.target.value})
  }
  _setIndicatorTag = (tagId) => {
    this.setState({indicatorTag: tagId})
  }
  _setCampaignType = (event) => {
    this.setState({campaignType: event.target.value})
  }

  render = () => {

    const campaign = this.props.campaign

    console.log('campaign', campaign)
    let nameSet = (
      <div>
        <label htmlFor='name'>Name: </label>
        <input type='text' defaultValue={campaign.name} onBlur={this._setCampaignName} ref='campaignName'/>
      </div>
    )

    // let topLevelLocationSet = (
    //   <div>
    //     <label htmlFor='top_lvl_location'>Top level location: </label>
    //     <DropdownButton
    //       items={this.state.locations}
    //       sendValue={CampaignPageActions.setLocation}
    //       item_plural_name='Locations'
    //       text={this.state.locationSelected[0] && this.state.locationSelected[0].name || 'Select Location'}
    //       icon='fa-globe'
    //       uniqueOnly/>
    //   </div>
    // )

    // let topLevelIndicatorTagSet = (
    //   <div>
    //     <label htmlFor='top_lvl_indicator_tag'>Top level indicator tag: </label>
    //     <DropdownButton
    //       items={this.state.indicatorToTags}
    //       sendValue={this._setIndicatorTag}
    //       item_plural_name='Indicator Tags'
    //       text={this.state.tagSelected[0] && this.state.tagSelected[0].tag_name || 'Select Tag'}
    //       icon='fa-tag'/>
    //   </div>
    // )

    // let campaignTypeSet = (
    //   <div>
    //     <label htmlFor='campaign_type'>Campaign type: </label>
    //     <select value={this.state.postData.campaign_type_id} onChange={this._setCampaignType}>
    //       {this.state.campaignTypes.map(d => {
    //         return d.id === this.state.postData.campaign_type_id
    //           ? (<option value={d.id} selected>{d.name}</option>)
    //           : (<option value={d.id}>{d.name}</option>) })}
    //     </select>
    //   </div>
    // )

    // let dateRangePicker = (
    //   <div>
    //     <label htmlFor='start_date'>Start date: </label>
    //     <DateMultiSelect
    //       start={this.state.campaign.start}
    //       end={this.state.campaign.end}
    //       sendValue={CampaignPageActions.updateCampaignRange}
    //       text='End date: ' />
    //   </div>
    // )

    // let submitButton = (
    //   <div>
    //     <br />
    //     <button className='tiny' onClick={this._save}>Save</button>
    //   </div>
    // )

    // let message = this.state.displayMsg
    //   ? (
    //     <div className={`message${this.state.saveSuccess ? ' success' : ' error'}`}>
    //       {this.state.message}
    //     </div>
    //   )
    //   : null

    return campaign ? (
      <div>
        <h2>Campaign ID: {campaign.id}</h2>
        <form>
          {nameSet}
          {/*topLevelLocationSet*/}
          {/*topLevelIndicatorTagSet*/}
          {/*campaignTypeSet*/}
          {/*dateRangePicker*/}
          {/*submitButton*/}
        </form>
      </div>
    ) : <Placeholder />
  }
}

// CampaignDetail.defaultProps = {
//   campaign: null,
//   columnDefs: [
//     {headerName: "ID", field: "id"},
//     {headerName: "Title", field: "title"},
//   ]
// }

// CampaignDetail.propTypes = {
//   campaign: PropTypes.object
// }

export default CampaignDetail
