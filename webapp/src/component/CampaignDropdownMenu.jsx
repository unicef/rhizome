'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var DropdownMenu     = require('component/DropdownMenu.jsx');
var CampaignMenuItem = require('component/CampaignMenuItem.jsx');

function searchValue(campaign) {
  var m = moment(campaign.start_date);

  // Include several possible date formats for matching against
  return [
    m.format('YYYY-MM'),
    m.format('MM-YYYY'),
    m.format('YYYY-M'),
    m.format('M-YYYY'),
    m.format('MMMM YYYY'),
    m.format('YYYY/MM'),
    m.format('MM/YYYY'),
    m.format('YYYY/M'),
    m.format('M/YYYY'),

    m.format('YY-MM'),
    m.format('MM-YY'),
    m.format('YY-M'),
    m.format('M-YY'),
    m.format('MMMM YY'),
    m.format('YY/MM'),
    m.format('MM/YY'),
    m.format('YY/M'),
    m.format('M/YY'),
  ].join(' ');
}

var CampaignDropdownMenu = React.createClass({
  propTypes : {
    campaigns : React.PropTypes.array.isRequired,
    sendValue : React.PropTypes.func.isRequired
  },

  getInitialState : function () {
    return {
      pattern : ''
    };
  },
  shouldComponentUpdate: function(nextProps, nextState) {
      return (nextProps.campaigns.length !== this.props.campaigns.length || nextProps.text !==this.props.text);
  },

  render : function () {
    var self = this;

    var re = new RegExp(this.state.pattern);
    console.log('CAMPAIGN props LENGTH: ', this.props.campaigns.length)

    // If the pattern is longer than two characters, filter the list with it,
    // otherwise, return true to include all campaigns in the dropdown
    var filterCampaigns = !_.isEmpty(this.state.pattern)?
      _.flow(searchValue, function (v) { return re.test(v); }) :
      _.constant(true);

    var campaigns = _(this.props.campaigns)
      // .uniq(false, function (c) { return moment(c.start_date).format('YYYYMM'); })

      // JD commenting this out because in the mapping screen we need to be able
      // to show camapigns with the same start date in different offices.

      // Uniquenss is handled at the database level ( campaign_type_id,
      // office_id, start_Date), thus the line of code below is unecessary

      .filter(filterCampaigns)
      .sortBy(_.method('start_date.getTime'))
      .map(function (campaign) {
        return (
          <CampaignMenuItem key={'campaign-' + campaign.id}
            sendValue={self.props.sendValue}
            {...campaign} />
        );
      })
      .value();

    var props = _.omit(this.props, 'campaigns', 'sendValue');

    return (
      <DropdownMenu icon='fa-calendar'
        searchable={true}
        onSearch={this._setPattern}
        {...props}>

        {campaigns}

      </DropdownMenu>
    );
  },

  _setPattern : function (value) {
    this.setState({ pattern : value })
  }
});

module.exports = CampaignDropdownMenu;
