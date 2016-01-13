import React from 'react'
import Reflux from 'reflux'

import LocationDropdownMenu from 'component/LocationDropdownMenu.jsx'
import List from 'component/list/List.jsx'

import EntryFormStore from 'stores/EntryFormStore'
import EntryFormActions from 'actions/EntryFormActions'

let EntryForm = React.createClass({
  mixins: [Reflux.connect(EntryFormStore)],

  getInitialState: function () {
    return {
      indicatorSets: require('./structure/indicator_sets')
    }
  },

  componentWillMount: function () {
    EntryFormActions.getCampaigns()
    EntryFormActions.getLocations()
  },

  _setIndicator: function (event) {
    EntryFormActions.setIndicator(event.target.value)
  },

  _setCampaign: function (event) {
    EntryFormActions.setCampaign(event.target.value)
  },

  render () {
    let indicatorSet = (
      <div>
        <label htmlFor='sets'>Indicator Set</label>
        <select value={this.state.indicatorSelected} onChange={this._setIndicator}>
          {this.state.indicatorSets.map(data => {
            return (<option value={data.id}>{data.title}</option>)
          })}
        </select>
      </div>
    )

    let campaignSet = (
      <div>
        <label htmlFor='campaigns'>Campaign</label>
        <select value={this.state.campaignSelected} onChange={this._setCampaign}>
          {this.state.campaigns.map(campaign => {
            return (<option value={campaign.value}>{campaign.text}</option>)
          })}
        </select>
      </div>
    )

    let locationSet = (
      <div>
        <label htmlFor='locations'>Locations</label>
        <LocationDropdownMenu
          locations={this.state.filterLocations}
          text='Select Location'
          sendValue={EntryFormActions.addLocations}
          style='databrowser__button' />
        <List items={this.state.locationSelected} removeItem={EntryFormActions.removeLocation} />
      </div>
    )

    let includeSublocations = (
      <div>
        <br />
        <label className={this.state.couldLoad ? '' : 'disabled'}>
          <input type='checkbox'
            checked={this.state.includeSublocations && this.state.couldLoad}
            onClick={EntryFormActions.changeSelect} />Include Sublocations
        </label>
      </div>
    )

    let loadEntryForm = (
      <div>
        <br />
        <a role='button'
          onClick={this.refresh}
          className={this.state.couldLoad ? 'button success' : 'button success disabled'} >
          <i className='fa fa-fw fa-refresh' />Load Entry Form
        </a>
      </div>
    )

    return (
      <div>
        <form className='row'>
          <div className='medium-2 columns'>
            {indicatorSet}
            {campaignSet}
            {locationSet}
            {includeSublocations}
            {loadEntryForm}
          </div>
        </form>
      </div>
    )
  }
})

export default EntryForm
