'use strict';

var _ = require('lodash');

function dashboardInit(dashboard, data, region, campaign, regionList, indicators, features) {
  var results = {};

  var indicatorsById = _.indexBy(indicators, 'id');
  var regionsById    = _.indexBy(regionList, 'id')

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

    var chartData = _.filter(data,
      // FIXME: should also filter by date since two charts could have the same
      // indicators but for different time periods
      d => _.includes(chart.indicators, d.indicator.id) &&
        _.get(d, regionProp) === region.id
    );

    if (_.endsWith(chart.type, 'Map')) {
      // Make sure we only get data for the current campaign; maps can't
      // display historical data. Index by region for quick lookup.
      var dataIdx = _(chartData)
        .filter(d => d.campaign.id === campaign.id)
        .indexBy('region.id')
        .value();

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

    results[sectionName] = section;
  });

  if (_.size(results) < 2) {
    // Use a simple array if there is only one section
    results = _(results).values().flatten().first();
  }

  return results;
}

module.exports = dashboardInit;
