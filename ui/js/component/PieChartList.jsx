'use strict';

var _ = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

var PieChartList = React.createClass({
  propTypes : {
    data      : React.PropTypes.array.isRequired,
    keyPrefix : React.PropTypes.string.isRequired,
    options   : React.PropTypes.object,
    name      : React.PropTypes.func
  },

  getDefaultProps : function () {
    return {
      name : _.property('indicator.short_name')
    };
  },

  render : function () {
    var pies = _.map(this.props.data, (d, i) => (
        <tr key={this.props.keyPrefix + '-' + i}>
          <td><Chart type='PieChart' data={d} options={this.props.options} /></td>
          <td>{this.props.name(d)}</td>
        </tr>
      )
    );

    if (_.isEmpty(pies)) {
      pies = (<tr><td>No data</td></tr>);
    }

    return (
      <table className='accessibility pie-charts'>{pies}</table>
    );
  },

});

module.exports = PieChartList;
