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
    var indicators = _.reject(this.props.indicators, ind => _.isEmpty(ind.bound_json));

    var targets = _(indicators)
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

    var scale = d3.scale.ordinal()
      .domain(['bad', 'okay', 'ok', 'good', 'invalid'])
      .range(['#AF373E', '#959595', '#959595','#2B8CBE', '#2D2525']);

    var data = _.map(this.props.data['district-heat-map'], s => (
      { name : s.name, values : _.filter(s.values, d => _.isFinite(d.value)) }
    ));

    var visible = _(data)
      .pluck('values')
      .flatten()
      .groupBy('indicator.id')
      .mapValues(v => _(v).pluck('value').some(_.isFinite))
      .value();

    var headers = this.state.showEmpty ?
      indicators :
      _.filter(indicators, i => visible[i.id]);

    var options = {
      cellSize   : 36,
      fontSize   : 14,
      headers    : headers,
      headerText : _.property('short_name'),
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
