'use strict';

var _ = require('lodash');
var d3 = require('d3');
var moment = require('moment');
var React = require('react');

var colors = require('colors');

var Chart = require('component/Chart.jsx');

var DashboardActions = require('actions/DashboardActions');

var series = function (values, name) {
  return {
    name: name,
    values: _.sortBy(values, _.result('campaign.start_date.getTime'))
  };
};

var indicatorForCampaign = function (campaign, indicator) {
  return d => d.campaign.id === campaign && d.indicator.id === indicator;
};

var HomepageCharts = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false
    };
  },

  generateMissedChildrenChartData: function (originalData) {
    var stack = d3.layout.stack()
      .order('default')
      .offset('zero')
      .values(_.property('values'))
      .x(_.property('campaign.start_date'))
      .y(_.property('value'));

    var missed;
    try {
      missed = _(originalData)
        .groupBy('indicator.short_name')
        .map(series)
        .thru(stack)
        .value();
    } catch (err) {
      console.error(err);
      console.log(`Data error in ${originalData}`);
      missed = [];
    }

    return missed;
  },

  render: function () {
    var data = this.props.data;
    var campaign = this.props.campaign;
    var upper = moment(campaign.start_date, 'YYYY-MM-DD');
    var lower = upper.clone().startOf('month').subtract(1, 'year');
    var loading = this.props.loading;

    var missed = this.generateMissedChildrenChartData(data.missedChildren);

    var missedScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 1),
      _.method('getTime')
    );

    var social = _.find(data.microplans, indicatorForCampaign(campaign.id, 28));
    social = !_.isEmpty(social) ? [[social]] : [];

    var planned = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 204)), 'value');
    var inPlace = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 175)), 'value');
    var withSM = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 176)), 'value');

    var transitPoints = [];
    if (!_.any([inPlace, planned], _.isUndefined)) {
      transitPoints.push([{
        title: inPlace + ' / ' + planned + ' in place',
        value: inPlace / planned
      }]);
    }

    if (!_.any([withSM, inPlace], _.isUndefined)) {
      transitPoints.push([{
        title: withSM + ' / ' + inPlace + ' have a social mobilizer',
        value: withSM / inPlace
      }]);
    }

    var pct = d3.format('%');

    var missedChildrenMap = data.missedChildrenByProvince;

    return (
        <div>
            <div className="large-4 columns chart-container" id="afghanistan-chart">
                <div className="chart">
                    <h5>Afghanistan</h5>
                    <carousel>
                        <Chart type='ChoroplethMap'
                             data={missedChildrenMap}
                             loading={loading}
                             options={{
                          domain  : _.constant([0, 0.1]),
                          value   : _.property('properties[475]'),
                          yFormat : d3.format('%'),
                          onClick : d => { DashboardActions.navigate({ location : d }) }
                        }}/>
                    </carousel>
                    <div className="chart-button-group">
                        <div className="chart-button"><span>Country overview</span></div>
                        <div className="chart-button"><span>District summary</span></div>
                    </div>
                </div>
            </div>
                
            <div className="large-4 columns chart-container" id="pakistan-chart">
                <div className="chart">
                    <h5>Pakistan</h5>
                    <carousel>
                        <Chart type='ColumnChart' data={missed}
                               loading={loading}
                               options={{
                            aspect  : 2.26,
                            color   : _.flow(_.property('name'), d3.scale.ordinal().range(colors)),
                            domain  : _.constant(missedScale),
                            x       : d => moment(d.campaign.start_date).startOf('month').valueOf(),
                            xFormat : d => moment(d).format('MMM YYYY'),
                            yFormat : pct
                          }}/>
                    </carousel>
                    <div className="chart-button-group">
                        <div className="chart-button"><span>Country overview</span></div>
                        <div className="chart-button"><span>District summary</span></div>
                    </div>
                </div>
            </div>
            <div className="large-4 columns chart-container" id="nigeria-chart">
                <div className="chart">
                    <h5>Nigeria</h5>
                    <carousel>
                    </carousel>
                    <div className="chart-button-group">
                        <div className="chart-button"><span>Country overview</span></div>
                        <div className="chart-button"><span>District summary</span></div>
                        <div className="chart-button"><span>NGA Campaign Monitoring</span></div>
                    </div>
                </div>
            </div>
        </div>
    );
  }
});

module.exports = HomepageCharts;
