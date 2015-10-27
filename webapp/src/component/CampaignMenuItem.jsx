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
    fromArray : function (arr, sendValue) {
      return arr.map(function (campaign) {
        var date = moment(campaign.start_date, 'YYYY-MM-DD').toDate();
        return (
          <CampaignMenuItem key={'campaign-' + campaign.id}
            sendValue={sendValue}
            id={campaign.id}
            slug={campaign.slug}
            management_dash_pct_complete={campaign.management_dash_pct_complete}/>
        );
      });
    }
  },

  render : function () {
    var campaignSlug = this.props.slug
    var percentageComplete = ' (' + Math.round(this.props.management_dash_pct_complete * 100) + '% complete)'

    return (
      <li key={'campaign-' + this.props.id} className='campaign'>
        <a role='menuitem' onClick={this._onClick}>
        {this.props.slug} {percentageComplete}
        </a>
      </li>
    );
  },

  _onClick : function () {
    this.props.sendValue(this.props.id);
  }

});

module.exports = CampaignMenuItem;
