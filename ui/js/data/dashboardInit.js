'use strict';

var _      = require('lodash');
var moment = require('moment');

/**
 * Recursively determine if child is a child of parent region.
 */
function childOf(parent, child) {
  if (!child) {
    return false;
  }

  if (parent.id === child.id) {
    return true;
  }

  return childOf(parent, child.parent);
}

function inChart(chart, campaign, region, datum) {
  var dt       = moment(datum.campaign.start_date).valueOf()
  var end      = moment(campaign.start_date, 'YYYY-MM-DD');
  var start    = chart.hasOwnProperty('timeRange') ?
    end.clone().subtract(chart.timeRange).valueOf() :
    -Infinity;

  var inPeriod = dt >= start && dt <= end.valueOf();

  var inRegion = false;

  switch (chart.region) {
    case 'subregions':
      inRegion = childOf(region, datum.region);

      if (!_.isEmpty(chart.level)) {
        inRegion = inRegion && chart.level === datum.region.region_type;
      }
      break;

    default:
      inRegion = region.id === datum.region.id;
      break;
  }

  return _.includes(chart.indicators, datum.indicator.id) && inPeriod && inRegion;
}

function choropleth(chart, data, campaign, features) {
  // Make sure we only get data for the current campaign; maps can't
  // display historical data. Index by region for quick lookup.
  var dataIdx = _(data)
    .filter(d => d.campaign.id === campaign.id)
    .indexBy('region.id')
    .value();

  _.each(features, f => {
    var d = dataIdx[f.properties.region_id];
    if (d) {
      f.properties[d.indicator.id] = d.value;
    }
  });

  return features;
}

function series(chart, data) {
  return _(data)
    .groupBy(chart.series)
    .map((values, name) => ({ name, values }))
    .value();
}

function scatter(chart, data, campaign) {
  return _(data)
    .filter(d => d.campaign.id === campaign.id)
    .groupBy('region.id')
    .map(values => {
      return _.reduce(values, (result, d) => {
        _.defaults(result, d);

        result[d.indicator.id] = d.value;

        return _.omit(result, 'indicator', 'value');
      }, {});
    })
    .filter(d => _(d).omit('region', 'campaign').values().all(_.isFinite))
    .value();
}

var process = {
  'BarChart'        : series,
  'ChoroplethMap'   : choropleth,
  'ColumnChart'     : series,
  'LineChart'       : series,
  'PieChart'        : series,
  'ScatterChart'    : scatter,
};

function dashboardInit(dashboard, data, region, campaign, regionList, indicators, features) {
  var results = {};

  var indicatorsById = _.indexBy(indicators, 'id');
  var regionsById    = _.indexBy(regionList, 'id');

  // Merge region metadata into the properties object of each geographic feature
  _.each(features, function (f) {
    var id = f.properties.region_id;
    _.assign(f.properties, regionsById[id]);
  });

  // Fill in indicators and regions on all the data objects. If we haven't
  // loaded indicators yet, continue displaying charts as if we have no data
  _.each(data, function (d) {
    var ind = indicatorsById[d.indicator];
    if (ind) {
      d.indicator = ind;
    }

    var reg = regionsById[d.region];
    if (reg) {
      d.region = reg;
    }
  });

  // Build up an object representing the data where each property of the object
  // corresponse to a section in the dashboard. Each section is an object where
  // each property corresponds to a chart. Each chart is an array of the data
  // that can be used by that chart
  _.each(dashboard.charts, (chart, i) => {
    var sectionName = _.get(chart, 'section', '__none__');
    var chartName   = _.get(chart, 'id', _.camelCase(chart.title));
    var section     = _.get(results, sectionName, {});
    var regionProp  = chart.region === 'subregions' ?
      'region.parent_region_id' :
      'region.id';

    var datumInChart   = _.partial(inChart, chart, campaign, region);
    section[chartName] = process[chart.type](
      chart,
      _.filter(data, datumInChart),
      campaign,
      features
    );

    results[sectionName] = section;
  });

  if (_.size(results) < 2) {
    // Use a simple array if there is only one section
    results = _(results).values().flatten().first();
  }

  return results;
}

module.exports = dashboardInit;
