'use strict';

var _ = require('lodash');
var React = require('react');
var Reflux = require('reflux');
var page = require('page');
var moment = require('moment');

var api = require('data/api');
var dashboardInit = require('data/dashboardInit');
var builtins = require('dashboard/builtin');

var DashboardStore = require('stores/DashboardStore');
var DataStore = require('stores/DataStore');
var GeoStore = require('stores/GeoStore');
var IndicatorStore = require('stores/IndicatorStore');
var NavigationStore = require('stores/NavigationStore');

var AppActions = require('actions/AppActions');
var DashboardActions = require('actions/DashboardActions');
var DataActions = require('actions/DataActions');
var GeoActions = require('actions/GeoActions');

var HomepageChartsSection = React.createClass({
    mixins: [
        Reflux.ListenerMixin,
        Reflux.connect(DataStore)
    ],

    getInitialState: function () {
        return {
            locations: [],
            campaigns: [],
            location: null,
            campaign: null,
            dashboard: null,
            allDashboards: builtins
        };
    },

    componentWillMount: function () {
        this._showDefault();
        AppActions.init();
    },

    componentDidMount: function () {
        this.listenTo(DashboardStore, this._onDashboardChange);
    },

    _onDashboardChange: function (state) {
        this.setState(state);

        if (this.state.loaded && this.state.location) {
            var q = DashboardStore.getQueries();

            if (_.isEmpty(q)) {
                DataActions.clear();
            } else {
                DataActions.fetch(this.state.campaign, this.state.location, q);
            }

            if (this.state.hasMap) {
                GeoActions.fetch(this.state.location);
            }
        }
    },

    _getDashboard: function (slug) {
        var dashboard = _.find(this.state.allDashboards, d => _.kebabCase(d.title) === slug);
        if (dashboard.id <= 0) {
            return new Promise(resolve => {
                resolve(dashboard)
            })
        }
    },

    _showDefault: function () {
      var self = this;
      this._getDashboard(this.props.dashboard).then(dashboard => {
          DashboardActions.setDashboard({
              dashboard,
              location: self.props.location,
              date: self.props.date
          });
      });
    },

    render: function () {
        if (!(this.state.loaded && this.state.dashboard)) {
            var style = {
                fontSize: '2rem'
            };

            return (
                <div style={style} className='overlay'>
                    <div>
                        <div><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
                    </div>
                </div>
            );
        }

        var {campaign, loading, location} = this.state;

        var dashboardDef = this.state.dashboard;

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
            location,
            campaign,
            this.state.locations,
            indicators,
            GeoStore.features
        );

        var homepageData = {
            data: data,
            campaign: campaign,
            loading: loading
        };

        var dashboard = React.createElement(require('dashboard/homepage/HomepageCharts.jsx'), homepageData);

        var chartId = `${this.props.location.toLowerCase()}-chart`;
        return (
            <div>
                <div className="large-4 columns chart-container" id={chartId}>
                    <div className="chart">
                        <h5>{this.props.location}</h5>
                          {dashboard}
                        <div className="chart-button-group">
                            <div className="chart-button"><span>Country overview</span></div>
                            <div className="chart-button"><span>District summary</span></div>
                        </div>
                    </div>
                </div>

            </div>
        );
    }

});

module.exports = HomepageChartsSection;
