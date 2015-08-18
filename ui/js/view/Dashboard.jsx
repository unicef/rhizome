'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');
var page   = require('page');
var moment = require('moment');

var api           = require('data/api');
var dashboardInit = require('data/dashboardInit');

var TitleMenu           = require('component/TitleMenu.jsx');
var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var CampaignTitleMenu   = require('component/CampaignTitleMenu.jsx');
var MenuItem            = require('component/MenuItem.jsx');

var CustomDashboard     = require('dashboard/CustomDashboard.jsx');

var DashboardStore      = require('stores/DashboardStore');
var GeoStore            = require('stores/GeoStore');
var IndicatorStore      = require('stores/IndicatorStore');
var NavigationStore     = require('stores/NavigationStore');

var AppActions          = require('actions/AppActions');
var DashboardActions    = require('actions/DashboardActions');
var DataActions         = require('actions/DataActions');
var GeoActions          = require('actions/GeoActions');

var LAYOUT = {
  'Management Dashboard'    : require('dashboard/ManagementDashboard.jsx'),
  'NGA Campaign Monitoring' : require('dashboard/NCODashboard.jsx'),
  'District Dashboard'      : require('dashboard/District.jsx'),
  'Source Data'      : require('dashboard/SourceDataDashboard.jsx')
};

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
    page('/datapoints/:dashboard', this._showDefault);
    AppActions.init();
  },

  componentWillUpdate : function (nextProps, nextState) {
    if (!(nextState.campaign && nextState.region && nextState.dashboard)) {
      return;
    }

    var campaign = moment(nextState.campaign.start_date).format('MM/YYYY')
    var title = [
      nextState.dashboard.title,
      [nextState.region.name, campaign].join(' '),
      'RhizomeDB'
    ].join(' - ');

    if (document.title !== title) {
      document.title = title;
    }
  },

  render : function () {
    if (!(this.state.loaded && this.state.dashboard)) {
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

    var campaign      = this.state.campaign;
    var dashboardDef  = this.state.dashboard;
    var loading       = this.state.loading;
    var region        = this.state.region;
    var dashboardName = _.get(dashboardDef, 'title', '');

    var indicators = IndicatorStore.getById.apply(
      IndicatorStore,
      _(_.get(dashboardDef, 'charts', []))
        .pluck('indicators')
        .flatten()
        .uniq()
        .value()
    );

    var data = dashboardInit(
      dashboardDef,
      this.state.data,
      region,
      campaign,
      this.state.regions,
      indicators,
      GeoStore.features
    );

    var dashboardProps = {
      campaign   : campaign,
      dashboard  : dashboardDef,
      data       : data,
      indicators : indicators,
      loading    : loading,
      region     : region
    };

    var dashboard = React.createElement(
      _.get(LAYOUT, dashboardName, CustomDashboard),
      dashboardProps);

    var campaigns = _(this.state.campaigns)
      .filter(c => c.office_id === region.office_id)
      .sortBy('start_date')
      .reverse()
      .value();

    if (campaign.office_id !== region.office_id) {
      campaign = campaigns[0];
    }

    var dashboardItems = MenuItem.fromArray(
      _.map(NavigationStore.dashboards, d => {
        return {
          title : d.title,
          value : _.kebabCase(d.title)
        };
      }),
      this._setDashboard);

    var edit;
    if (dashboardDef.owned_by_current_user) {
      edit = (
        <span>
          <a className='menu-button fa-stack'
            href={'/datapoints/dashboards/edit/' + dashboardDef.id + '/'}>
            <i className='fa fa-stack-2x fa-circle'></i>
            <i className='fa fa-stack-1x fa-pencil'></i>
          </a>
          &emsp;
        </span>
      );
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

            <div className='medium-4 columns'>
              <h2 style={{ textAlign: 'right' }}>
                {edit}
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

    this.navigateUnsubscribe = this.listenTo(
      DashboardActions.navigate,
      this._navigate);

    this.navigationStoreUnsubscribe = this.listenTo(
      NavigationStore,
      this._onNavigationChange);
  },

  componentWillUnmount : function () {
    this.dashboardUnsubscribe();
    this.indicatorUnsubscribe();
    this.geoUnsubscribe();
    this.navigateUnsubscribe();
    this.navigationStoreUnsubscribe();
  },

  _onDashboardChange : function (state) {
    var fetchData = this.state.loaded;

    this.setState(state);

    if (fetchData) {
      var q = DashboardStore.getQueries();

      if (_.isEmpty(q)) {
        DataActions.clear();
      } else {
        DataActions.fetch(this.state.campaign, this.state.region, q);
      }

      if (this.state.hasMap) {
        GeoActions.fetch(this.state.region);
      }
    } else if (NavigationStore.loaded) {
      page({ click : false });
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

    this._navigate({ campaign : moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM') });
  },

  _setRegion : function (id) {
    var region    = _.find(this.state.regions, r => r.id === id)

    if (!region) {
      return;
    }

    this._navigate({ region : region.name });
  },

  _setDashboard : function (slug) {
    this._navigate({ dashboard : slug });
  },

  _onNavigationChange : function (nav) {
    if (NavigationStore.loaded && DashboardStore.loaded) {
      page({ click : false });
    }
  },

  _navigate : function (params) {
    var slug     = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title));
    var region   = _.get(params, 'region', this.props.region.name);
    var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'));

    if (_.isNumber(region)) {
      region = _.find(this.state.regions, r => r.id === region).name;
    }

    page('/datapoints/' + [slug, region, campaign].join('/'));
  },

  _showDefault : function (ctx) {
    var dashboard = NavigationStore.getDashboard(ctx.params.dashboard);

    DashboardActions.setDashboard({ dashboard });
  },

  _show : function (ctx) {
    var dashboard = NavigationStore.getDashboard(ctx.params.dashboard);

    DashboardActions.setDashboard({
      dashboard,
      region : ctx.params.region,
      date   : [ctx.params.year, ctx.params.month].join('-')
    });
  }
});

module.exports = Dashboard;
