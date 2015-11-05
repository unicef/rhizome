'use strict';

var _ = require('lodash');
var React = require('react');

var moment = require('moment');

var CampaignMenuItem = React.createClass({
  propTypes : {
    sendValue  : React.PropTypes.func.isRequired,
    id         : React.PropTypes.number.isRequired,
    slug       : React.PropTypes.string.isRequired,
  },

  statics : {
    fromArray : function (arr, location, sendValue) {
      return arr.map(function (campaign) {
        return (
          <CampaignMenuItem
            campaign={campaign}
            location={location.name}
            sendValue={sendValue} />
        );
      });
    }
  },

  render : function () {
    var percentageComplete = ' (' + Math.round(this.props.campaign.management_dash_pct_complete * 100) + '% complete)';
    var date = moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('MMMM YYYY');

    return (
      <li key={'campaign-' + this.props.campaign.id} className='campaign'>
        <a role='menuitem' onClick={this._onClick}>
          {this.props.location} {date} {percentageComplete}
        </a>
      </li>
    );
  },

  _onClick : function () {
    this.props.sendValue(this.props.campaign.id);
  }

});

module.exports = CampaignMenuItem;
