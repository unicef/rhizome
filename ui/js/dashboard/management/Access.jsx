'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var Chart = require('component/Chart.jsx');

var Access = React.createClass({
  propTypes : {
    campaign   : React.PropTypes.object.isRequired,
    data       : React.PropTypes.array.isRequired,
    indicators : React.PropTypes.object.isRequired,
  },

  render : function () {
    var data         = _(this.props.data);
    var inaccessible = data.filter(d => d.indicator.id === 158)
      .sortBy(_.method('campaign.start_date.getTime'))
      .groupBy('indicator.short_name')
      .map(function (values, name) {
        return { name : name, values : values };
      })
      .value();

    var m     = moment(this.props.campaign.start_date, 'YYYY-MM-DD')
    var lower = m.clone().startOf('month').subtract(1, 'year');
    var upper = m.clone().endOf('month');

    var options = {
      aspect  : 2.572,
      domain  : _.constant([lower.toDate(), upper.toDate()]),
      values  : _.property('values'),
      x       : _.property('campaign.start_date'),
      y       : _.property('value'),
      yFormat : d3.format(',.0f')
    };

    return (
      <div className='medium-2 columns'>
        <h3>Access Challenged Districts</h3>
        <h6>Number of Inaccessible Children</h6>

        <Chart type='LineChart' data={inaccessible} options={options} />

        <div className='row'>

        </div>
      </div>
    );
  },
});

module.exports = Access;
