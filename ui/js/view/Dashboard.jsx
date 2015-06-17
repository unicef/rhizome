'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');
var page   = require('page');
var moment = require('moment');

var api = require('data/api');

var ManagementDashboard = require('dashboard/ManagementDashboard.jsx');
var NCODashboard        = require('dashboard/NCODashboard.jsx');

var TitleMenu           = require('component/TitleMenu.jsx');
var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var CampaignTitleMenu   = require('component/CampaignTitleMenu.jsx');
var MenuItem            = require('component/MenuItem.jsx');

var DashboardStore      = require('stores/DashboardStore');
var GeoStore            = require('stores/GeoStore');
var IndicatorStore      = require('stores/IndicatorStore');

var AppActions          = require('actions/AppActions');
var DashboardActions    = require('actions/DashboardActions');
var DataActions         = require('actions/DataActions');
var GeoActions          = require('actions/GeoActions');

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
      var style = {
        fontSize      : '2rem',
      };

      return (
        <div style={style} className='overlay'>
          <div>
            <div><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
          </div>
        </div>
      );
    }

    var campaign     = this.state.campaign;
    var dashboardDef = this.state.dashboard;
    var loading      = this.state.loading;
    var region       = this.state.region;

    var data = {};

    var dashboardName = _.get(dashboardDef, 'title', '');
    var dashboard     = '';

    var indicators = _.indexBy(
      IndicatorStore.getById.apply(IndicatorStore,
        _(_.get(dashboardDef, 'charts', [])).pluck('indicators').flatten().uniq().value()),
      'id');

    var features = GeoStore.features;

    if (!_.isEmpty(indicators)) {
      var regionsById = _.indexBy(this.state.regions, 'id')

      // Fill in indicators and regions on all the data objects. If we haven't
      // loaded indicators yet, continue displaying charts as if we have no data
      _.each(this.state.data, function (d) {
        var ind = indicators[d.indicator];
        if (ind) {
          d.indicator = ind;
        }

        var reg = regionsById[d.region];
        if (reg) {
          d.region = reg;
        }
      });

      // Indicator index: maps indicator IDs to one or more sections containing
      _.each(dashboardDef.charts, (chart, i) => {
        var sectionName = _.get(chart, 'section', '__none__');
        var chartName   = _.camelCase(_.get(chart, 'title', i));
        var section     = _.get(data, sectionName, {});
        var regionProp  = chart.region === 'subregions' ?
          'region.parent_region_id' :
          'region.id';

        var chartData = _.filter(this.state.data,
          d => _.includes(chart.indicators, d.indicator.id) &&
            _.get(d, regionProp) === region.id
        );

        if (_.endsWith(chart.type, 'Map')) {
          var dataIdx = _.indexBy(chartData, 'region.id');

          _.each(features, f => {
            var d = dataIdx[f.properties.region_id];
            if (d) {
              f.properties[d.indicator.id] = d.value;
            }
          });

          section[chartName] = features;
        } else {
          section[chartName] = chartData
        }

        data[sectionName] = section;
      });

      if (_.size(data) < 2) {
        // Use a simple array if there is only one section
        data = _(data).values().flatten().value();
      }
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

      case 'NGA Campaign Monitoring':
        dashboard = (
          <NCODashboard
            dashboard={dashboardDef}
            loading={loading}
            region={region}
            data={data} />
        );
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

    var dashboardItems = MenuItem.fromArray(
      _.map(this.state.dashboards, d => {
        return {
          title : d.title,
          value : _.kebabCase(d.title)
        };
      }),
      this._setDashboard);

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

            <div className='medium-4 columns'>
              <h2 style={{ textAlign: 'right' }}>
                <TitleMenu text={dashboardName}>
                  {dashboardItems}
                </TitleMenu>
              </h2>
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

    this.geoUnsubscribe = this.listenTo(
      GeoStore,
      this._onGeographyLoaded);
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

    if (state.hasMap) {
      GeoActions.fetch(state.region);
    }
  },

  _onIndicatorsChange : function () {
    this.forceUpdate();
  },

  _onGeographyLoaded : function () {
    this.forceUpdate();
  },

  _setCampaign : function (id) {
    var campaign  = _.find(this.state.campaigns, c => c.id === id);

    if (!campaign) {
      return;
    }

    var dashboard = _.kebabCase(this.state.dashboard.title);
    var region    = this.state.region.name;

    page('/datapoints/' + [dashboard, region, moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM')].join('/'));
  },

  _setRegion : function (id) {
    var campaign  = moment(this.state.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM');
    var dashboard = _.kebabCase(this.state.dashboard.title);
    var region    = _.find(this.state.regions, r => r.id === id)

    if (!region) {
      return;
    }

    page('/datapoints/' + [dashboard, region.name, campaign].join('/'));
  },

  _setDashboard : function (slug) {
    var campaign = moment(this.state.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM');
    var region   = this.state.region.name;

    page('/datapoints/' + [slug, region, campaign].join('/'));
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
