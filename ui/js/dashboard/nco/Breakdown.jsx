'use strict';

var _     = require('lodash');
var React = require('react');

var ToggleableStackedBar = require('dashboard/ToggleableStackedBar.jsx');

function prep (data) {
  return _(data)
    .groupBy('region.id')
    .filter(v => _(v).pluck('value').some(_.isFinite))
    .flatten()
    .groupBy('indicator.short_name')
    .map((v, n) => { return { name : n, values : v }; })
    .value();
}

var Breakdown = React.createClass({
  propTypes : {
    data    : React.PropTypes.object.isRequired,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var data    = this.props.data;
    var loading = this.props.loading;

    var options = {
      x : _.property('value'),
      y : _.property('region.name'),
      margin : {
        top    : 0,
        right  : 80,
        bottom : 18,
        left   : 80
      }
    }

    return (
      <div>
        <div className='row'>
          <div className='medium-8 columns'>
            <ToggleableStackedBar
              title='Missed Children'
              loading={loading}
              options={options}
              data={prep(data.missedChildren)} />
          </div>
        </div>

        <div className='row'>
          <div className='medium-6 columns'>
            <ToggleableStackedBar
              title='Absences'
              loading={loading}
              options={options}
              data={prep(data.absences)} />
          </div>

          <div className='medium-6 columns'>
            <ToggleableStackedBar
              title='Non-Compliance'
              loading={loading}
              options={options}
              data={prep(data.nonCompliance)} />
          </div>
        </div>

        <div className='row'>
          <div className='medium-4 columns'>
            <ToggleableStackedBar
              title='Non-Compliance Resolutions'
              loading={loading}
              options={options}
              data={prep(data.nonComplianceResolutions)} />
          </div>

          <div className='medium-4 columns'>
            <ToggleableStackedBar
              title='Influencers'
              loading={loading}
              options={options}
              data={prep(data.influencers)} />
          </div>

          <div className='medium-4 columns'>
            <ToggleableStackedBar
              title='Sources of Information'
              loading={loading}
              options={options}
              data={prep(data.sourcesOfInformation)} />
          </div>
        </div>

      </div>
    );
  },

});

module.exports = Breakdown;
