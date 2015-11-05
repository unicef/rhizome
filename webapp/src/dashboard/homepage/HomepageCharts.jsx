'use strict';

var _ = require('lodash');
var d3 = require('d3');
var moment = require('moment');

var React = require('react');
var Carousel = require('nuka-carousel');
var HomepageCarouselDecorators = require('./HomepageCarouselDecorators.jsx');

var colors = require('colors');
var Chart = require('component/Chart.jsx');
var YtDChart = require('component/YtDChart.jsx');

var series = function (values, name) {
  return {
    name: name,
    values: _.sortBy(values, _.result('campaign.start_date.getTime'))
  };
};

var indicatorForCampaign = function (campaign, indicator) {
  return d => d.campaign.id === campaign && d.indicator.id === indicator;
};

function percentage(dataset) {
  var total = _(dataset).pluck('value').sum();

  _.forEach(dataset, function (d) {
    d.value /= total;
  });

  return dataset;
}

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

  preparePolioCasesData: function() {
    var campaign   = this.props.campaign;
    var year       = '';
    var month      = '';
    var totalCases = null;
    var newCases   = null;

    if (campaign) {
      var m = moment(campaign.start_date, 'YYYY-MM-DD');
      year  = m.format('YYYY');
      month = m.format('MMM');

      // Sum all of the reported Polio cases for the year
      totalCases = _(this.props.data.impact.polioCasesYtd)
        .filter(function (d) { return d.campaign.start_date.getFullYear() == year; })
        .pluck('value')
        .sum();

      // Find the number of reported cases for this campaign
      newCases = _.get(
        _.find(
          this.props.data.impact.polioCasesYtd,
          function (d) { return d.campaign.start_date.getTime() === m.valueOf();}),
        'value');
    }

    // Set the title based on whether there is data
    var title = <h4 className="chart-title">
        <span style={{
          'color': '#F18448'
        }}>{totalCases} Polio cases this year</span>
      </h4>;

    var newCaseLabel = '';

    if (_.isFinite(newCases) && newCases > 0) {
      var plural = newCases !== 1 ? 's' : '';
      newCaseLabel = (
        <div id='new-polio-cases'
          style={{
            position :'absolute',
            color: '#D84E43'
          }}>{newCases} new case{plural}</div>
      );
    }

    var color = d3.scale.ordinal()
      .range(['#AF373E', '#525b5e', '#82888e', '#98a0a8', '#b6c0cc'])
      .domain(_(this.props.data.impact.polioCasesYtd)
        .map(_.method('campaign.start_date.getFullYear'))
        .uniq()
        .sortBy()
        .reverse()
        .value());

    return {
      title: title,
      newCaseLabel: newCaseLabel,
      data: this.props.data.impact.polioCasesYtd,
      colors: color
    }
  },

  preparePerformanceData: function() {
    var data = this.props.data.performance;
    var campaign = this.props.campaign;
    var location = this.props.location;

    var upper = moment(campaign.start_date, 'YYYY-MM-DD');
    var lower = upper.clone().startOf('month').subtract(1, 'year');

    var missed = this.generateMissedChildrenChartData(data.missedChildren);

    var missedScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 1),
      _.method('getTime')
    );

    var missedChildrenMap = data.missedChildrenByProvince;

    return {
      missedChildrenMap: missedChildrenMap,
      missed: missed,
      missedScale: missedScale,
      location: location
    };
  },

  prepareUnderImmunizedData: function () {
    var stack = d3.layout.stack()
      .offset('zero')
      .values(function (d) { return d.values; })
      .x(function (d) { return d.campaign.start_date; })
      .y(function (d) { return d.value; });

    var data = _(this.props.data.impact.underImmunizedChildren)
      .each(function (d) {
        // Add a property to each datapoint indicating the fiscal quarter
        d.quarter = moment(d.campaign.start_date).format('[Q]Q YYYY');
      })
      .groupBy(function (d) {
        return d.indicator.id + '-' + d.quarter;
      })
      .map(function (datapoints) {
        // Calculate the total number of children with X doses of OPV for
        // each quarter
        return _.assign({}, datapoints[0], {
          'value' : _(datapoints).pluck('value').sum()
        });
      })
      .groupBy('quarter')
      .map(percentage)
      .flatten()
      .reject(function (d) {
        // Exclude 4+ doses, because that is implied as 1 - <0 doses> - <1–3 doses>
        return d.indicator.id === 433;
      })
      .groupBy('indicator.short_name')
      .map(function (values, name) {
        return {
          name   : name,
          values : values
        };
      })
      .sortBy('name')
      .value();

    var start = moment(this.props.campaign.start_date);
    var lower = start.clone().startOf('quarter').subtract(3, 'years');
    var upper = start.clone().endOf('quarter');

    var immunityScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 3),
      _.method('getTime')
    );

    var color = _.flow(
      _.property('name'),
      d3.scale.ordinal()
        .domain(_(data).pluck('name').sortBy().value())
        .range(['#AF373E', '#FABAA2'])
    );

    return {
      data: stack(data),
      immunityScale: immunityScale,
      color: color
    };
  },

  prepareChartsData: function() {
    var pct = d3.format('%');

    var loading = this.props.loading;

    var charts = [];

    var performanceData = this.preparePerformanceData();
    var underImmunizedData = this.prepareUnderImmunizedData();
    var polioCasesData = this.preparePolioCasesData();

    charts.push(
      <div id='polio-cases-ytd'>
        {polioCasesData.title}
        <div style={{ position : 'relative' }}>
          {polioCasesData.newCaseLabel}
          <YtDChart
            data={polioCasesData.data}
            loading={loading}
            options={{
              color  : _.flow(_.property('name'), polioCasesData.colors),
              aspect  : 1,
              width: 390,
              height: 390
            }} />
          </div>
        </div>
    );

    charts.push(
      <div>
        <h4 className="chart-title">Missed children, {performanceData.location}</h4>
        <Chart type='ChoroplethMap'
        data={performanceData.missedChildrenMap}
        loading={loading}
        options={{
          domain  : _.constant([0, 0.1]),
          value   : _.property('properties[475]'),
          yFormat : d3.format('%'),
          width: 390,
          height: 390
        }}
      />
      </div>
      );

    charts.push(
      <div>
        <h4 className="chart-title">Missed children, trend</h4>
        <Chart type='ColumnChart' data={performanceData.missed}
          loading={loading}
          options={{
            aspect  : 1,
            color   : _.flow(_.property('name'), d3.scale.ordinal().range(colors)),
            domain  : _.constant(performanceData.missedScale),
            x       : d => moment(d.campaign.start_date).startOf('month').valueOf(),
            xFormat : d => moment(d).format('MMM YYYY'),
            yFormat : pct,
            width: 390,
            height: 390
          }}
        />
      </div>);

    charts.push(
      <div>
        <h4 className="chart-title">Under Immunized Children</h4>
        <Chart type='ColumnChart'
          data={underImmunizedData.data}
          loading={loading}
          options={{
            aspect  : 1,
            color   : underImmunizedData.color,
            domain  : _.constant(underImmunizedData.immunityScale),
            values  : _.property('values'),
            x       : function (d) { return moment(d.campaign.start_date).startOf('quarter').valueOf(); },
            xFormat : function (d) { return moment(d).format('[Q]Q [ ]YYYY'); },
            y0      : _.property('y0'),
            yFormat : d3.format(',.1%'),
            width: 390,
            height: 390
          }}
        />
      </div>);

    return _.shuffle(charts);
  },

  render: function () {
    var list = this.prepareChartsData();

    return (
      <Carousel decorators={HomepageCarouselDecorators}>
          {list}
      </Carousel>
    );
  }
});

module.exports = HomepageCharts;
