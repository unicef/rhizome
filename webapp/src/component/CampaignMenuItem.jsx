import React from 'react'

var CampaignMenuItem = React.createClass({
  propTypes: {
    sendValue: React.PropTypes.func.isRequired,
    campaign: React.PropTypes.object.isRequired
  },

  statics: {
    fromArray: function (arr, sendValue) {
      return arr.map(function (campaign) {
        return (
          <CampaignMenuItem
            campaign={campaign}
            sendValue={sendValue} />
        )
      })
    }
  },

  render: function () {
    var percentageComplete = ' (' + Math.round(this.props.campaign.management_dash_pct_complete * 100) + '% complete)'

    return (
      <li key={'campaign-' + this.props.campaign.id} className='campaign'>
        <a role='menuitem' onClick={this._onClick}>
          {this.props.campaign.slug} {percentageComplete}
        </a>
      </li>
    )
  },

  _onClick: function () {
    this.props.sendValue(this.props.campaign.id)
  }

})

export default CampaignMenuItem
