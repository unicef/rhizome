'use strict';

var _ = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

var District = React.createClass({
  getInitialState : function () {
    return {
      showEmpty : false
    };
  },

  render : function () {
    // Hash of indicators that have bounds defined for easy filtering
    var indicators = _(this.props.indicators)
      .indexBy('id')
      .mapValues(ind => !_.isEmpty(ind.bound_json))
      .value();

    // List of indicator definitions based on the hash of indicator IDs who
    // have bounds defined
    var indicatorList = _.filter(this.props.indicators, ind => indicators[ind.id]);

    // Map indicator IDs to a d3 threshold scale for determining into what
    // target range a value falls for a given indicator
    var targets = _(indicatorList)
      .indexBy('id')
      .mapValues(ind => {
        var bounds = _(ind.bound_json)
          .map(b => [b.bound_name, _.isNumber(b.mn_val) ? b.mn_val : -Infinity])
          .sortBy('1');

        var extents = bounds.pluck('1').slice(1).value();
        var names   = bounds.pluck('0').value();

        return d3.scale.threshold()
          .domain(extents)
          .range(names);
      })
      .value();

    // Scale for coloring based on pre-defined values
    var scale = d3.scale.ordinal()
      .domain(['bad', 'okay', 'ok', 'good', 'invalid'])
      .range(['#AF373E', '#959595', '#959595','#2B8CBE', '#2D2525']);

    // Clean the data by first removing any data whose values are not finite -
    // i.e. undefined - or whose indicators have no target bounds defined, then
    // remove any series (rows) that have no data
    var data = _(this.props.data['district-heat-map'])
      .map(s => ({
        name : s.name,
        values : _.filter(s.values, d => indicators[d.indicator.id] && _.isFinite(d.value))
      }))
      .reject(s => _.isEmpty(s.values))
      .value();

    // Hash indicator IDs to a boolean indicating whether that column is
    // non-empty (true) or empty (false)
    var visible = _(data)
      .pluck('values')
      .flatten()
      .groupBy('indicator.id')
      .mapValues(v => _(v).pluck('value').some(_.isFinite))
      .value();

    // Determine what headers are shown based on whether or not the "Show empty
    // columns" checkbox is on
    var headers = this.state.showEmpty ?
      indicatorList :
      _.filter(indicatorList, i => visible[i.id]);

    var options = {
      cellSize   : 36,
      fontSize   : 14,
      headers    : headers,
      scale      : d => scale(_.get(targets, d.indicator.id, _.noop)(d.value)),
      value      : _.property('range'),
    };

    return (
      <div id='district-dashboard'>
        <div className='row'>
          <form className='small-12 columns'>
            <label>
              <input type='checkbox'
                checked={this.state.showEmpty}
                onChange={this._setShowEmpty} />
              Show empty columns
            </label>
          </form>
        </div>

        <div className='row'>
          <div className='small-12 columns'>
            <Chart type='HeatMapChart'
              loading={this.props.loading}
              data={data}
              options={options} />
          </div>
        </div>
      </div>
    );
  },

  _setShowEmpty : function (evt) {
    this.setState({ showEmpty : evt.target.checked });
  }
});

module.exports = District;
