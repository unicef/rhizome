'use strict';

var _ = require('lodash');
var React = require('react');

var moment = require('moment');

var CampaignMenuItem = React.createClass({
  propTypes : {
    sendValue  : React.PropTypes.func.isRequired,

    id         : React.PropTypes.number.isRequired,
    start_date : React.PropTypes.instanceOf(Date).isRequired,
  },

  statics : {
    fromArray : function (arr, sendValue) {
      return arr.map(function (campaign) {
        var date = moment(campaign.start_date, 'YYYY-MM-DD').toDate();

        return (
          <CampaignMenuItem key={'campaign-' + campaign.id}
            sendValue={sendValue}
            id={campaign.id}
            start_date={date}
            pct_complete={campaign.pct_complete}/>
        );
      });
    }
  },

  render : function () {
    var m                    = moment(this.props.start_date);
    var start_date           = m.format('YYYY-MM-DD');
    var formatted_start_date = m.format('MMMM YYYY');
    var pct_complete_string  = '-' + Math.round(this.props.pct_complete * 100) + '% complete'

    return (
      <li key={'campaign-' + this.props.id} className='campaign'>
        <a role='menuitem' onClick={this._onClick}>
        {formatted_start_date} {pct_complete_string}
        </a>
      </li>
    );
  },

  _onClick : function () {
    this.props.sendValue(this.props.id);
  }

});

module.exports = CampaignMenuItem;
