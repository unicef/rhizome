'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');
var React  = require('react');

var colors       = require('colors');

var Chart        = require('component/Chart.jsx');
var PieChartList = require('component/PieChartList.jsx');

function series(values, name) {
  return {
    name   : name,
    values : _.sortBy(values, _.result('campaign.start_date.getTime'))
  };
}
var Performance = React.createClass({

  propTypes : {
    campaign : React.PropTypes.object.isRequired,
    data     : React.PropTypes.array
  },

  getDefaultProps : function () {
    return {
      data : []
    };
  },

  render : function () {
    var data     = _(this.props.data);
    var campaign = this.props.campaign;
    var upper    = moment(campaign.start_date, 'YYYY-MM-DD');
    var lower    = upper.clone().startOf('month').subtract(1, 'year');

    var stack = d3.layout.stack()
      .order('default')
      .offset('zero')
      .values(_.property('values'))
      .x(_.property('campaign.start_date'))
      .y(_.property('value'));

    var missed = data
      .filter(d => _.includes([166,164,167,165], d.indicator.id))
      .groupBy('indicator.short_name')
      .map(series)
      .thru(stack)
      .value();

    var missedScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 1),
      _.method('getTime')
    );

    var conversions = data
      .filter(d => _.includes([187,189], d.indicator.id))
      .groupBy('indicator.short_name')
      .map(series)
      .value();

    var social = data.find(d => d.campaign.id === campaign.id && d.indicator.id === 28);
    var microplans = data.find(d => d.campaign.id === campaign.id && d.indicator.id === 27);

    var microplansText = function () {
      var num = _.get(social, '[0][0].value');
      var den = _.get(microplans, 'value');

      return _.isFinite(num) && _.isFinite(den) ?
        num + ' / ' + den + ' microplans incorporate social data' :
        '';
    }

    social = !_.isEmpty(social) ? [[social]] : [];

    var vaccinated = '';
    var transitPoints = [];

    var pct = d3.format('%');

    return (
      <div>
        <div className='medium-5 columns'>
          <h3>Performance of Front Line Workers</h3>
        </div>

        <div className='medium-2 columns'>
          <section>
            <h4>Missed Children</h4>
            <Chart type='ColumnChart' data={missed}
              options={{
                aspect  : 2.26,
                color   : _.flow(_.property('name'), d3.scale.ordinal().range(colors)),
                domain  : _.constant(missedScale),
                x       : d => moment(d.campaign.start_date).startOf('month').valueOf(),
                xFormat : d => moment(d).format('MMM YYYY'),
                yFormat : pct
              }} />
          </section>

          <section>
            <h4>Conversions</h4>
            <Chart type='LineChart' data={conversions} options={{
              aspect  : 2.26,
              domain  : _.constant([lower.toDate(), upper.toDate()]),
              yFormat : pct
            }} />
          </section>

          <section>
            <PieChartList
              keyPrefix='microplans'
              data={social}
              name={microplansText}
              options={{
                domain : _.constant([0, _.get(microplans, 'value', 1)]),
                size   : 32
              }} />
          </section>
        </div>

        <section className='medium-2 columns'>
          <h4>Missed Children</h4>
        </section>

        <section className='transit-points medium-1 column'>
          <h4>Transit Points</h4>

          {vaccinated}

          <PieChartList keyPrefix='transit-points' data={transitPoints} />
        </section>
      </div>
    );
  },
});

module.exports = Performance;
