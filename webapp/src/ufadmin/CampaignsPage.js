import React from 'react'
import Reflux from 'reflux'
import DateRangePicker from 'component/DateTimePicker.jsx'

import CampaignPageActions from 'actions/CampaignPageActions'
import CampaignPageStore from 'stores/CampaignPageStore'

var CampaignsPage = React.createClass({
  mixins: [Reflux.connect(CampaignPageStore)],

  propTypes: {
    campaignId: React.PropTypes.number
  },

  componentWillMount: function () {
    var id = this.props.campaignId
    CampaignPageActions.initialize(id)
  },
  _setOffice: function (event) {
    CampaignPageActions.setOffice(event.target.value)
  },
  _setCampaignName: function (event) {
    CampaignPageActions.setCampaignName(event.target.value)
  },
  _setLocation: function (event) {
    CampaignPageActions.setLocation(event.target.value)
  },
  _setIndicatorTag: function (event) {
    CampaignPageActions.setIndicatorTag(event.target.value)
  },
  _setCampaignType: function (event) {
    CampaignPageActions.setCampaignType(event.target.value)
  },
  _save: function (e) {
    e.preventDefault()
    var today = new Date().toJSON().slice(0, 10)
    this.state.postData['start_date'] = this.state.campaign.start ? this.state.campaign.start : today
    this.state.postData['end_date'] = this.state.campaign.end ? this.state.campaign.end : today
    CampaignPageActions.saveCampaign(this.state.postData)
  },
  render: function () {
    let officeSet = (
      <div>
        <label htmlFor='office'>Office: </label>
        <select value={this.state.postData.office_id} onChange={this._setOffice}>
          {this.state.offices.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let nameSet = (
      <div>
        <label htmlFor='name'>Name: </label>
        <input type='text' value={this.state.postData.name} onChange={this._setCampaignName}/>
      </div>
    )

    let topLevelLocationSet = (
      <div>
        <label htmlFor='top_lvl_location'>Top level location: </label>
        <select value={this.state.postData.top_lvl_location_id} onChange={this._setLocation}>
          {this.state.locations.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let topLevelIndicatorTagSet = (
      <div>
        <label htmlFor='top_lvl_indicator_tag'>Top level indicator tag: </label>
        <select value={this.state.postData.top_lvl_indicator_tag_id} onChange={this._setIndicatorTag}>
          {this.state.indicatorToTags.map(d => { return (<option value={d.id}>{d.tag_name}</option>) })}
        </select>
      </div>
    )

    let campaignTypeSet = (
      <div>
        <label htmlFor='campaign_type'>Campaign type: </label>
        <select value={this.state.postData.campaign_type_id} onChange={this._setCampaignType}>
          {this.state.campaignTypes.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let dateRangePicker = (
      <div>
        <label htmlFor='start_date'>Start date: </label>
        <DateRangePicker
          start={this.state.campaign.start}
          end={this.state.campaign.end}
          sendValue={CampaignPageActions.updateCampaignRange}
          text='End date: ' />
      </div>
    )

    let submitButton = (
      <div>
        <br />
        <button className='tiny' onClick={this._save}>Save</button>
      </div>
    )

    let message = this.state.displayMsg
      ? (
        <div className={`message${this.state.saveSuccess ? ' success' : ' error'}`}>
          {this.state.message}
        </div>
      )
      : null

    return (
      <div className='row'>
        <div className='large-4 large-offset-4 columns'>
          <h2>Manage Campaign Page</h2>
          {message}
          <form>
            {officeSet}
            {nameSet}
            {topLevelLocationSet}
            {topLevelIndicatorTagSet}
            {campaignTypeSet}
            {dateRangePicker}
            {submitButton}
          </form>
        </div>
      </div>
    )
  }
})

export default CampaignsPage
