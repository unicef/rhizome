'use strict';

var _     = require('lodash');
var React = require('react');
var Reflux = require('reflux/src');
var page  = require('page');
var moment = require('moment');

var api = require('data/api');

var ManagementDashboard = require('dashboard/ManagementDashboard.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
var DropdownMenu = require('component/DropdownMenu.jsx');
var MenuItem = require('component/MenuItem.jsx');
var DashboardActions = require('actions/DashboardActions');

var Dashboard = React.createClass({
  mixins : [Reflux.connect(require('stores/DashboardStore'))],

  getInitialState : function () {
    return {
      regions      : [],
      campaigns    : [],
      region       : null,
      campaign     : null,
      regionFilter : null,
      dashboard    : null
    };
  },

  componentWillMount : function () {
    page('/datapoints/:dashboard/:region/:year/:month', this._show);
    page({ click : false });
  },

  render : function () {
    var region = this.state.region;

    var campaign = this.state.campaign;

    var campaignSelection = campaign ?
      moment(campaign.start_date, 'YYYY-MM-DD').format('MMM YYYY') :
      '';

    var regionSelection = _.get(region, 'name', '');

    var dashboardName = _.get(this.state, 'dashboard.title', '');

    var dashboard = '';

    switch (dashboardName) {
      case 'Management Dashboard':
        dashboard = (
          <ManagementDashboard campaign={campaign} region={region} />
        );
        break;

      default:
        break;
    }

    var campaigns = this.state.campaigns;

    var re = !_.isEmpty(this.state.regionFilter) ?
      new RegExp(this.state.regionFilter, 'gi') :
      null;

    var regionList = re ?
      _.filter(this.state.regions, function (r) {
        return re.test(r.name);
      }) :
      this.state.regions;

    var regions = MenuItem.fromArray(
      _.map(regionList, function (r) {
        return {
          title : r.name,
          value : r.id
        };
      }),
      this._setRegion
    );

    return (
      <div>
        <div classNameName='clearfix'></div>

        <form className='inline no-print'>
          <div className='row'>
            <div className='medium-6 columns'>
              <h1>
                {/*<CampaignDropdownMenu
                  text={campaignSelection}
                  campaigns={campaigns}
                  sendValue={this._setCampaign} />*/}
                <DropdownMenu
                  icon='fa-globe'
                  text={regionSelection}
                  searchable={true}
                  onSearch={this._setRegionFilter}>
                  {regions}
                </DropdownMenu>
              </h1>
            </div>

            <div className='medium-6 columns'>
              <h2>{dashboardName}</h2>
            </div>
          </div>
        </form>

        {dashboard}
      </div>
    );
  },

  componentDidMount : function () {

  },

  _setCampaign : function (id) {
    this.setState({ campaign : this.state.campaigns[id] });
  },

  _setRegion : function (id) {
    this.setState({ region : this.state.regions[id] });
  },

  _setRegionFilter : function (pattern) {
    this.setState({ regionFilter : pattern });
  },

  _show : function (ctx) {
    DashboardActions.setDashboard({
      dashboard : ctx.params.dashboard,
      region    : ctx.params.region,
      date      : [ctx.params.year, ctx.params.month].join('-')
    });
  }
});

module.exports = Dashboard;
