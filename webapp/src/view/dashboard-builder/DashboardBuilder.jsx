'use strict';

var _ = require('lodash');
//var moment = require('moment');
var React = require('react');
var DragDropMixin = require('react-dnd').DragDropMixin;
var Reflux = require('reflux/src');
var ChartBuilder = require('view/chart-builder/ChartBuilder.jsx');
var ChartWizard = require('view/chart-wizard/ChartWizard.jsx');

var dashboardInit = require('data/dashboardInit');

var DataActions = require('actions/DataActions');
var DataStore = require('stores/DataStore');

var DashboardBuilderActions = require('actions/DashboardBuilderActions');
var DashboardBuilderStore = require("stores/DashboardBuilderStore");

var DashboardActions = require('actions/DashboardActions');
var DashboardStore = require("stores/DashboardStore");

var IndicatorStore = require('stores/IndicatorStore');
var GeoStore = require('stores/GeoStore');
var GeoActions = require('actions/GeoActions');
var AppActions = require('actions/AppActions');
var RegionTitleMenu = require('component/RegionTitleMenu.jsx');
var CampaignTitleMenu = require('component/CampaignTitleMenu.jsx');
var TitleInput = require('component/TitleInput.jsx');

var CustomDashboard = require('dashboard/CustomDashboard.jsx');

var moment = require('moment');

window.perf = React.addons.Perf;

module.exports = React.createClass({
  mixins: [Reflux.connect(DashboardBuilderStore, "store"),
    Reflux.connect(DataStore, "dataStore"),
    Reflux.connect(DashboardStore, "dashboardStore"),
    Reflux.ListenerMixin
  ],
  componentWillMount: function () {
    AppActions.init();
  },
  componentDidMount: function () {
    DashboardBuilderActions.initialize(this.props.dashboard_id);
    this.listenTo(DashboardStore, this._onDataLoaded);
    this.listenTo(DashboardBuilderStore, this._onDataLoaded);
    this.listenTo(DashboardStore, this._onDashboardChange);
    this.indicatorUnsubscribe = this.listenTo(IndicatorStore, this._onIndicatorsChange);

  },
  getInitialState: function () {
    return {
      chartBuilderActive: false,
      chartBuilderindex: null,
      title: '',
      description: ''
    }
  },
  editChart: function (index) {
    this.setState({chartBuilderindex: index, chartBuilderActive: true});
  },
  cancelEditChart: function () {
    this.setState({chartBuilderindex: null, chartBuilderActive: false});
  },
  moveForward: function (index) {
    DashboardBuilderActions.moveForward(index);
  },
  moveBackward: function (index) {
    DashboardBuilderActions.moveBackward(index);
  },
  deleteChart: function (index) {
    var chart = _.get(this.state, 'store.dashboard.charts[' + index + '].title', '');

    if (_.isEmpty(chart)) {
      chart = 'this chart';
    } else {
      chart = '"' + chart + '"';
    }

    var dashboard = _.get(this.state, 'store.dashboard.title', '');
    if (_.isEmpty(dashboard)) {
      dashboard = 'the dashboard';
    }

    if (window.confirm('Delete ' + chart + ' from ' + dashboard + '?')) {
      // FIXME
      DashboardBuilderActions.removeChart(index);
    }
  },
  _deleteDashboard: function () {
    if (window.confirm('Delete dashboard "' + this.state.store.dashboardTitle + '"?')) {
      // FIXME
      DashboardBuilderActions.deleteDashboard();
    }
  },
  newChart: function () {
    this.setState({chartBuilderindex: null, chartBuilderActive: true});
  },
  saveChart: function (chartDef) {
    if (!_.isNull(this.state.chartBuilderindex)) {
      DashboardBuilderActions.updateChart(chartDef, this.state.chartBuilderindex);
    } else {
      DashboardBuilderActions.addChart(chartDef);
    }
    this.setState({chartBuilderindex: null, chartBuilderActive: false});
  },
  _onIndicatorsChange: function () {
    this.forceUpdate();
  },
  _onDashboardChange: function (state) {
    var dashboardSet = this.state.dashboardStore.dashboard;

    if (dashboardSet) {
      var q = DashboardStore.getQueries();

      if (_.isEmpty(q)) {
        DataActions.clear();
      } else {
        DataActions.fetch(this.state.dashboardStore.campaign, this.state.dashboardStore.location, q);
      }

      if (this.state.dashboardStore.hasMap) {
        GeoActions.fetch(this.state.dashboardStore.location);
      }
    }
  },
  _setCampaign: function (id) {
    var campaign = _.find(this.state.dashboardStore.campaigns, c => c.id === id);

    if (!!campaign) {
      DashboardActions.setDashboard({
        dashboard: this.state.store.dashboard,
        date: moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY-MM')
      });
    }
  },

  _setRegion: function (id) {
    var location = _.find(this.state.dashboardStore.locations, r => r.id === id)

    if (!!location) {
      DashboardActions.setDashboard({dashboard: this.state.store.dashboard, location: location.name});
    }
  },

  _onDataLoaded: function () {
    if (this.props.dashboard_id && this.state.store && this.state.dashboardStore && this.state.store.loaded && this.state.dashboardStore.loaded && !this.state.dashboardStore.dashboard) {
      DashboardActions.setDashboard({dashboard: this.state.store.dashboard});
      this.setState({title: this.state.store.dashboardTitle, description: this.state.store.dashboardDescription})
    }
  },

  _updateTitle: function (newText) {
    DashboardBuilderActions.updateTitle(newText);
  },

  _updateNewTitle: function (e) {
    this.setState({title: e.currentTarget.value});
    DashboardBuilderActions.updateTitle(e.currentTarget.value);
  },

  _updateDescription: function (newText) {
    DashboardBuilderActions.updateDescription(newText);
  },

  _handleSubmit: function (e) {
    e.preventDefault();
    DashboardBuilderActions.addDashboard();
  },

  render: function () {
    if (this.state.store.newDashboard) {
      return (<form className='inline no-print dashboard-builder-container' onSubmit={this._handleSubmit}>
        <h1>Create a New Custom Dashboard</h1>

        <div className="titleDiv">Dashboard Title</div>
        <input type="text" value={this.state.title} onChange={this._updateNewTitle}/>
        {this.state.store.dashboardTitle.length ?
          <a href="#" className="button next-button" onClick={DashboardBuilderActions.addDashboard}>Next</a> : null}
      </form>);
    }
    else if (!(this.state.dashboardStore && this.state.dashboardStore.loaded && this.state.dashboardStore.dashboard)) {
      var style = {
        fontSize: '2rem',
      };

      return (
        <div style={style} className='overlay'>
          <div>
            <div><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
          </div>
        </div>
      );
    }

    var self = this;
    var campaign = this.state.dashboardStore.campaign;
    var dashboardDef = this.state.store.dashboard;
    var loading = this.state.dashboardStore.loading;
    var location = this.state.dashboardStore.location;
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
      this.state.dataStore.data,
      location,
      campaign,
      this.state.dashboardStore.locations,
      indicators,
      GeoStore.features
    );
    var dashboardProps = {
      campaign: campaign,
      dashboard: dashboardDef,
      data: data,
      indicators: indicators,
      loading: loading,
      location: location,
      editable: true,
      onAddChart: this.newChart,
      onEditChart: this.editChart,
      onDeleteChart: this.deleteChart,
      onMoveForward: this.moveForward,
      onMoveBackward: this.moveBackward
    };

    var dashboard = React.createElement(
      CustomDashboard,
      dashboardProps);

    var campaigns = _(this.state.dashboardStore.campaigns)
      .filter(c => c.office_id === location.office_id)
      .sortBy('start_date')
      .reverse()
      .value();

    if (campaign.office_id !== location.office_id) {
      campaign = campaigns[0];
    }

    var addDashboardLinkContainer = (
      <div className="empty-dashboard-add-container">
        <a role='button' className='button' onClick={this.newChart}>
          <i className='fa fa-icon fa-fw fa-plus'></i>&ensp;Add New Chart to Dashboard
        </a>
      </div>
    );
    var dashboardBuilderContainer = (
      <div>
        <form className='inline no-print row cd-bg-color'>
          <div className='medium-6 columns'>
            <div className='medium-6 columns'>
              <CampaignTitleMenu
                campaigns={campaigns}
                selected={campaign}
                sendValue={this._setCampaign}/>
            </div>

            <div className='medium-6 columns'>
              <RegionTitleMenu
                locations={this.state.dashboardStore.locations}
                selected={location}
                sendValue={this._setRegion}/>
            </div>
          </div>

          <div className="medium-3 columns right">
            Dashboard Title
            <TitleInput initialText={this.state.title} save={this._updateTitle}/>
          </div>
        </form>
        {this.state.store.dashboard.charts.length ? null : addDashboardLinkContainer}
        {dashboard}

        <div className="dashboard-footer">
          <div className="right">
            <a role='button' className='button deleteButton' href='#' onClick={this._deleteDashboard}>
              <i className='fa fa-icon fa-fw fa-trash'></i>&ensp;Delete this dashboard
            </a>
          </div>

          <a role='button' className='button' onClick={this.newChart}>
            <i className='fa fa-icon fa-fw fa-plus'></i>&ensp;Add Chart
          </a>


		          <span>
		          	&ensp;
                Description

		              <TitleInput class="descriptionField" initialText={this.state.description}
                              save={this._updateDescription}/>
		          </span>

		          <span>
	              	&ensp;Changes are saved when you make them.
				  </span>

        </div>

      </div>
    );
    if (!this.state.store.loaded) {
      return (<div>loading</div>);
    }
    else if (this.state.chartBuilderActive) {
      var chartDef = (_.isNull(this.state.chartBuilderindex) ? null : this.state.store.dashboard.charts[this.state.chartBuilderindex]);
      return (
        <ChartWizard dashboardId={this.props.dashboard_id} chartDef={chartDef} save={this.saveChart}
                     cancel={this.cancelEditChart} campaign={campaign} location={location}/>
      )
    }
    else {
      return dashboardBuilderContainer;
    }
  }
});
