import React from 'react'
import moment from 'moment'
import DatePicker from 'component/DatePicker.jsx'

var CampaignsPage = React.createClass ({
  render: function () {
    let offices = [
      {
        id: 0,
        name: 'Af'
      },
      {
        id: 1,
        name: 'Ni'
      },
      {
        id: 2,
        name: 'Pa'
      }
    ]

    let officeSet = (
      <div>
        <label htmlFor='office'>Office: </label>
        <select>
          {offices.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let nameSet = (
      <div>
        <label htmlFor='name'>Name: </label>
        <input type='text'/>
      </div>
    )

    let locations = [
      {
        id: 1,
        name: 'brady'
      }
    ]

    let topLevelLocationSet = (
      <div>
        <label htmlFor='top_lvl_location'>Top level location: </label>
        <select>
          {locations.map(d => { return (<option value={d.id}>{d.name}</option>) })}
        </select>
      </div>
    )

    let indicators = [
      {
        id: 1,
        name: 'test indicator',
        short_name: 'test'
      }
    ]

    let topLevelIndicatorTagSet = (
      <div>
        <label htmlFor='top_lvl_indicator_tag'>Top level indicator tag: </label>
        <select>
          {indicators.map(d => { return (<option value={d.id}>{d.short_name}</option>) })}
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

    let startDate = moment('2015-02-01').toDate()
    let endDate = moment('2015-02-20').toDate()

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
        <div className="large-6 large-offset-3 columns">
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
