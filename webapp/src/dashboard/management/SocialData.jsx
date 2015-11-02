'use strict';

var _      = require('lodash');
var React  = require('react');

var DonutChart   = require('component/DonutChart.jsx');

var palette = require('colors');

var SocialData = React.createClass({
  propTypes : {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
  },

  render : function() {
    var data     = this.props.data;
    var campaign = this.props.campaign;
    var indicators = this.props.indicators;
    var loading  = this.props.loading;

    var planLabel = function (d) {
      var fmt = d3.format('%');
      var v   = _.get(d, '[0].value', '');

      return fmt(v);
    };

    return (
        <div className="row">
          <div className="medium-4 columns">
            <DonutChart data={data} label={planLabel}
              loading={loading}
              options={{
                innerRadius : 0.6,
                domain      : _.constant([0, 1]),
                palette     : palette
              }} />
          </div>
        </div>
    );
  }
});

module.exports = SocialData;