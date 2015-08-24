'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var TitleMenu        = require('component/TitleMenu.jsx');
var CampaignMenuItem = require('component/CampaignMenuItem.jsx');

var CampaignTitleMenu = React.createClass({
  propTypes : {
    campaigns : React.PropTypes.array.isRequired,
    selected  : React.PropTypes.object.isRequired,
    sendValue : React.PropTypes.func.isRequired
  },

  render : function () {
    var campaigns = CampaignMenuItem.fromArray(this.props.campaigns, this.props.sendValue);
    var startDate = moment(this.props.selected.start_date, 'YYYY-MM-DD').format('MMM YYYY');

    return (
      <TitleMenu
        icon='fa-calendar'
        text={startDate}>
        {campaigns}
      </TitleMenu>
    );
  },
});

module.exports = CampaignTitleMenu;
