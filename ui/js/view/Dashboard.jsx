'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');
var page   = require('page');
var moment = require('moment');

var api = require('data/api');

var ManagementDashboard  = require('dashboard/ManagementDashboard.jsx');

var RegionTitleMenu      = require('component/RegionTitleMenu.jsx');
var CampaignTitleMenu    = require('component/CampaignTitleMenu.jsx');

var DashboardStore       = require('stores/DashboardStore');
var IndicatorStore       = require('stores/IndicatorStore');

var AppActions           = require('actions/AppActions');
var DashboardActions     = require('actions/DashboardActions');
var DataActions          = require('actions/DataActions');

var Dashboard = React.createClass({
  mixins : [
    Reflux.ListenerMixin,
    Reflux.connect(require('stores/DataStore'))
  ],

  getInitialState : function () {
    return {
      regions      : [],
      campaigns    : [],
      region       : null,
      campaign     : null,
      dashboard    : null,
    };
  },

  componentWillMount : function () {
    page('/datapoints/:dashboard/:region/:year/:month', this._show);
    page({ click : false });
    AppActions.init();
  },

  render : function () {
    if (!this.state.loaded) {
      return (
        <div className='overlay'>
          <div>
            <div>
              <i className='fa fa-spinner fa-spin'></i>
              &ensp;loading
            </div>
          </div>
        </div>
      );
    }

    var campaign     = this.state.campaign;
    var dashboardDef = this.state.dashboard;
    var data         = this.state.data;
    var loading      = this.state.loading;
    var region       = this.state.region;

    var dashboardName   = _.get(dashboardDef, 'title', '');
    var dashboard       = '';

    var indicators = _.indexBy(
      IndicatorStore.getById.apply(IndicatorStore,
        _(_.get(dashboardDef, 'charts', [])).pluck('indicators').flatten().uniq().value()),
      'id');

    // Fill in indicators on all the data objects. If we haven't loaded
    // indicators yet, continue displaying charts as if we have no data
    if (!_.isEmpty(indicators)) {
      _.each(data, function (d) {
        var ind = indicators[d.indicator];
        if (ind) {
          d.indicator = ind;
        }
      });
    } else {
      data = [];
    }

    switch (dashboardName) {
      case 'Management Dashboard':
        dashboard = (
          <ManagementDashboard
            dashboard={dashboardDef}
            campaign={campaign}
            indicators={indicators}
            region={region}
            loading={loading}
            data={data} />
        );
        break;

      case 'District Dashboard':
        break;

      case 'NGA Campaign Monitoring':
        break;

      default:
        break;
    }

    var campaigns = _(this.state.campaigns)
      .filter(c => c.office_id === region.office_id)
      .sortBy('start_date')
      .reverse()
      .value();

    if (campaign.office_id !== region.office_id) {
      campaign = campaigns[0];
    }

    return (
      <div>
        <div classNameName='clearfix'></div>

        <form className='inline no-print'>
          <div className='row'>
            <div className='medium-6 columns'>
              <h1>
                <CampaignTitleMenu
                  campaigns={campaigns}
                  selected={campaign}
                  sendValue={this._setCampaign} />
                &emsp;
                <RegionTitleMenu
                  regions={this.state.regions}
                  selected={region}
                  sendValue={this._setRegion} />
              </h1>
            </div>

            <div className='medium-3 columns'>
              <h2>{dashboardName}</h2>
            </div>
          </div>
        </form>

        {dashboard}
      </div>
    );
  },

  componentDidMount : function () {
    this.dashboardUnsubscribe = this.listenTo(
      DashboardStore,
      this._onDashboardChange);

    this.indicatorUnsubscribe = this.listenTo(
      IndicatorStore,
      this._onIndicatorsChange);
  },

  componentWillUnmount : function () {
    this.dashboardUnsubscribe();
    this.indicatorUnsubscribe();
  },

  _onDashboardChange : function (state) {
    this.setState(state);

    var q = DashboardStore.getQueries();

    if (_.isEmpty(q)) {
      DataActions.clear();
    } else {
      DataActions.fetch(state.campaign, state.region, q);
    }
  },

  _onIndicatorsChange : function () {
    this.forceUpdate();
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
