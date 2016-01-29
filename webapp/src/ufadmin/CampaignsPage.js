import React from 'react'
import Reflux from 'reflux'
import moment from 'moment'
import DatePicker from 'component/DatePicker.jsx'

import CampaignPageActions from 'actions/CampaignPageActions'
import CampaignPageStore from 'stores/CampaignPageStore'

var CampaignsPage = React.createClass ({
  mixins: [Reflux.connect(CampaignPageStore)],

  componentWillMount: function () {
    CampaignPageActions.initData()
  },

  render: function () {
    let officeSet = (
      <div>
        <label htmlFor='office'>Office: </label>
        <select>
          {this.state.offices.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let nameSet = (
      <div>
        <label htmlFor='name'>Name: </label>
        <input type='text'/>
      </div>
    )

    let topLevelLocationSet = (
      <div>
        <label htmlFor='top_lvl_location'>Top level location: </label>
        <select>
          {this.state.locations.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let topLevelIndicatorTagSet = (
      <div>
        <label htmlFor='top_lvl_indicator_tag'>Top level indicator tag: </label>
        <select>
          {this.state.indicatorToTags.map(d => { return (<option value={d.id}>{d.tag_name}</option>) })}
        </select>
      </div>
    )

    let campaignTypes = [
      {
        id: 1,
        name: 'SIAD'
      }
    ]

    let campaignTypeSet = (
      <div>
        <label htmlFor='campaign_type'>Campaign type: </label>
        <select>
          {campaignTypes.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let startDate = moment(new Date()).toDate()
    let endDate = moment(new Date()).toDate()

    let startDatePicker = (
      <div>
        <label htmlFor='start_date'>Start date: </label>
        <DatePicker date={startDate} sendValue={null} />
      </div>
    )

    let endDatePicker = (
      <div>
        <label htmlFor='start_date'>End date: </label>
        <DatePicker date={endDate} sendValue={null} />
      </div>
    )

    let submitButton = (
      <div>
        <br />
        <button className='tiny'>Save</button>
      </div>
    )

    return (
      <div className='row'>
        <div className="large-4 large-offset-4 columns">
          <h2>Manage Campaign Page</h2>
          <form>
            {officeSet}
            {nameSet}
            {topLevelLocationSet}
            {topLevelIndicatorTagSet}
            {campaignTypeSet}
            {startDatePicker}
            <br />
            {endDatePicker}
            {submitButton}
          </form>
        </div>
      </div>
    )
  }
})

export default CampaignsPage
