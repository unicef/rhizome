'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var Chart        = require('component/Chart.jsx');
var DonutChart   = require('component/DonutChart.jsx');
var PieChartList = require('component/PieChartList.jsx');

var palette = require('colors');


var Access = React.createClass({
  propTypes : {
    campaign   : React.PropTypes.object.isRequired,
    indicators : React.PropTypes.object.isRequired,
    data       : React.PropTypes.object,
  },

  render : function () {
    var data     = this.props.data;
    var campaign = this.props.campaign;
    var loading  = this.props.loading;

    var inaccessible = _(data.numberOfInaccessibleChildren)
      .sortBy(_.method('campaign.start_date.getTime'))
      .groupBy('indicator.short_name')
      .map(function (values, name) {
        return { name : name, values : values };
      })
      .value();

    var reasons = _(data.inaccessibilityBreakdown)
      .filter(d => {
        return d.campaign.id === campaign.id &&
          _.isFinite(d.value) &&
          d.value >= 0.01;
      })
      .sortBy(_.property('value'))
      .reverse()
      .map(d => [d])
      .value();

    var pieChartName = function (d) {
      return d3.format('%')(d[0].value) + ' ' +
        _.trimLeft(d[0].indicator.short_name, '% ');
    };

    var plans = _.filter(data.districtsWithAccessPlans,
      d => d.campaign.id === campaign.id && _.isFinite(d.value));

    var planLabel = function (d) {
      var fmt = d3.format('%');
      var v   = _.get(d, '[0].value', '');

      return fmt(v);
    };

    var m     = moment(this.props.campaign.start_date, 'YYYY-MM-DD')
    var lower = m.clone().startOf('month').subtract(1, 'year');
    var upper = m.clone().endOf('month');

    var lineChartOptions = {
      aspect  : 2.572,
      domain  : _.constant([lower.toDate(), upper.toDate()]),
      values  : _.property('values'),
      x       : _.property('campaign.start_date'),
      y       : _.property('value'),
      yFormat : d3.format(',.0f')
    };

    return (
      <div className='medium-4 columns'>
        <h3>Inaccessible Children</h3>

        <div className="row">
          <div className="medium-4 columns">
            <h6>Number of Inaccessible Children</h6>
            <Chart type='LineChart' data={inaccessible}
            loading={loading}
            options={lineChartOptions} />
          </div>

          <div className='accessibility medium-2 columns'>
            <h6>Inaccessibiity Breakdown</h6>
            <PieChartList keyPrefix='inaccessibility-breakdown'
              loading={loading}
              data={reasons}
              name={pieChartName}
              options={{
                domain  : _.constant([0, 1]),
                size    : 16,
                palette : palette
              }} />
          </div>

          <div className='medium-2 columns'>
            <h6>Districts with Access Plan</h6>
            <DonutChart data={plans} label={planLabel}
              loading={loading}
              options={{
                innerRadius : 0.6,
                domain      : _.constant([0, 1]),
                palette     : palette
              }} />
          </div>

        </div>
      </div>
    );
  }
});

module.exports = Access;
