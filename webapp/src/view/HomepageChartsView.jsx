'use strict';

var _ = require('lodash');
var React = require('react');
var Reflux = require('reflux');
var page = require('page');
var moment = require('moment');

var api = require('data/api');
var dashboardInit = require('data/dashboardInit');
var builtins = require('dashboard/builtin');

var CustomDashboard = require('dashboard/CustomDashboard.jsx');

var DashboardStore = require('stores/DashboardStore');
var DataStore = require('stores/DataStore');
var GeoStore = require('stores/GeoStore');
var IndicatorStore = require('stores/IndicatorStore');
var NavigationStore = require('stores/NavigationStore');

var AppActions = require('actions/AppActions');
var DashboardActions = require('actions/DashboardActions');
var DataActions = require('actions/DataActions');
var GeoActions = require('actions/GeoActions');

var HomepageChartsView = React.createClass({
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
            allDashboards: []
        };
    },

    getAllDashboards: function() {
        var self = this;
        api.get_dashboard().then(function(response) {
            var customDashboards = _(response.objects).sortBy('title').value();
            var allDashboards = builtins.concat(customDashboards);
            self.setState({allDashboards: allDashboards});
            self._showDefault();
        });
    },

    componentWillMount: function () {
        this.getAllDashboards();
        AppActions.init();
    },

    componentWillUpdate: function (nextProps, nextState) {
        if (!(nextState.campaign && nextState.location && nextState.dashboard)) {
            return;
        }

        var campaign = moment(nextState.campaign.start_date).format('MM/YYYY')
        var title = [
            nextState.dashboard.title,
            [nextState.location.name, campaign].join(' '),
            'RhizomeDB'
        ].join(' - ');

        if (document.title !== title) {
            document.title = title;
        }
    },

    componentDidMount: function () {
        this.listenTo(DashboardStore, this._onDashboardChange);

        this.listenTo(IndicatorStore, () => this.forceUpdate());
        this.listenTo(GeoStore, () => this.forceUpdate());
    },

    _onDashboardChange: function (state) {
        var fetchData = this.state.loaded;

        this.setState(state);


        if (this.state.loaded) {
            var q = DashboardStore.getQueries();

            if (_.isEmpty(q)) {
                DataActions.clear();
            } else {
                DataActions.fetch(this.state.campaign, this.state.location, q);
            }

            if (this.state.hasMap) {
                GeoActions.fetch(this.state.location);
            }
        } else if (NavigationStore.loaded) {
            page({
                click: false
            });
        }
    },

    _getDashboard: function (slug) {
        var dashboard = _.find(this.state.allDashboards, d => _.kebabCase(d.title) === slug);
        if (dashboard.id <= 0) {
            return new Promise(resolve => {
                resolve(dashboard)
            })
        } else {
            return api.get_chart({dashboard_id: dashboard.id}, null, {'cache-control': 'no-cache'}).then(res => {
                dashboard.charts = res.objects.map(chart => {
                    var result = chart.chart_json;
                    result.id = chart.id;
                    return result;
                });
                return dashboard
            }, function (err) {
                console.log(err);
                dashboard.charts = [];
            });
        }
    },

    _showDefault: function () {
        this._getDashboard('management-dashboard').then(dashboard => {
            DashboardActions.setDashboard({
                dashboard,
                location: 'Nigeria',
                date: '2015-09'
            });
        })
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

        var {campaign, loading, location, doc_id, doc_tab} = this.state;

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

        var dashboardProps = {
            campaign: campaign,
            dashboard: dashboardDef,
            data: data,
            indicators: indicators,
            loading: loading,
            location: location,
            doc_tab: doc_tab,
            doc_id: doc_id
        };

        var homepageData = {
            data: data.performance,
            campaign: campaign,
            loading: loading
        };

        var dashboard = React.createElement(require('dashboard/homepage/HomepageCharts.jsx'), homepageData);

        return (
            <div>
                {dashboard}
            </div>
        );
    }

});

module.exports = HomepageChartsView;
