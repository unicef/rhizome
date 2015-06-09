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

  render : function () {
    var m                    = moment(this.props.start_date);
    var start_date           = m.format('YYYY-MM-DD');
    var formatted_start_date = m.format('MMMM YYYY');
    return (
      <li key={'campaign-' + this.props.id} className='campaign'>
        <a role='menuitem' onClick={this._onClick}>
          <time dateTime={start_date}>{formatted_start_date}</time>&emsp;
        </a>
      </li>
    );
  },

  _onClick : function () {
    this.props.sendValue(this.props.id);
  }

});

module.exports = CampaignMenuItem;
