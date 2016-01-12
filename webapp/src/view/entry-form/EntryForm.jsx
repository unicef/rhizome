import React from 'react'
import Reflux from 'reflux'

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
  },

  _setIndicator: function (event) {
    EntryFormActions.setIndicator(event.target.value)
  },

  _setCampaign: function (event) {
    EntryFormActions.setCampaign(event.target.value)
  },

  render () {
    let indicatorSet = (
      <div className='medium-2 columns'>
        <label htmlFor='sets'>Indicator Set</label>
        <select value={this.state.indicator_set_id} onChange={this._setIndicator}>
          {this.state.indicatorSets.map(data => {
            return (<option value={data.id}>{data.title}</option>)
          })}
        </select>
      </div>
    )

    let campaignSet = (
      <div className='medium-2 columns'>
        <label htmlFor='campaigns'>Campaign</label>
        <select value={this.state.campaign_id} onChange={this._setCampaign}>
          {this.state.campaigns.map(campaign => {
            return (<option value={campaign.value}>{campaign.text}</option>)
          })}
        </select>
      </div>
    )

    return (
      <div>
        <form className='inline'>
          <div className='row'>
            {indicatorSet}
            {campaignSet}
          </div>
        </form>
      </div>
    )
  }
})

export default EntryForm
