'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var Impact             = require('dashboard/management/Impact.jsx');
var Performance        = require('dashboard/management/Performance.jsx');
var Access             = require('dashboard/management/Access.jsx');
var BulletChartSection = require('./BulletChartSection.jsx');

var ManagementDashboard = React.createClass({
  propTypes : {
    dashboard  : React.PropTypes.object.isRequired,
    indicators : React.PropTypes.object.isRequired,

    campaign   : React.PropTypes.object,
    data       : React.PropTypes.oneOfType([
      React.PropTypes.array,
      React.PropTypes.object
    ]),
    loading    : React.PropTypes.bool,
    region     : React.PropTypes.object,
  },

  getDefaultProps : function () {
    return {
      data    : [],
      loading : true
    };
  },

  render : function () {
    var campaign   = this.props.campaign;
    var data       = this.props.data;
    var indicators = this.props.indicators;
    var loading    = this.props.loading;
    var region     = _.get(this.props, 'region.name', '');

    console.log('ManagementDashboard::data', data);

    var sections = _(this.props.dashboard.charts)
      .groupBy('section')
      .transform(function (result, charts, section) {
        result[section] = _(charts)
          .pluck('indicators')
          .flatten()
          .map(_.propertyOf(indicators))
          .value();
      })
      .value();

    return (
      <div id='management-dashboard'>
        <div className='row print-only'>
          <div className='small-12 columns'>
            <h1>
              <span className='campaign'>{ campaign }</span>
              <span className='region'>{ region }</span>
            </h1>
            <h2>
              Polio<br />
              Performance<br />
              Dashboard
            </h2>
            <img src='/static/img/UNICEF.svg' className='logo'/>
          </div>
        </div>

        <div className='row'>
          <Impact data={data.impact} campaign={this.props.campaign} loading={loading} />
          <Performance data={data.performance} campaign={this.props.campaign} loading={loading} />
        </div>

        <div className='row'>
          <section className='medium-2 columns'>
            <h3>FLWs' Capacity to Perform</h3>
            <BulletChartSection data={data.capacity} campaign={campaign} indicators={sections.capacity} loading={loading} cols={2} />
          </section>

          <div className='medium-1 column'>
            <h3>Supply</h3>
            <BulletChartSection data={data.supply} campaign={campaign} indicators={sections.supply} loading={loading} cols={1} />
          </div>

          <div className='medium-1 column'>
            <h3>Polio+</h3>
            <BulletChartSection data={data.polio} campaign={campaign} indicators={sections.polio} loading={loading} cols={1} />
          </div>

          <div className='medium-1 column'>
            <h3>Resources</h3>
            <BulletChartSection data={data.resources} campaign={campaign} indicators={sections.resources} loading={loading} cols={1} />
          </div>

          <Access data={data.access} campaign={campaign} indicators={indicators} loading={loading} />
        </div>

      </div>
    );
  },
});

module.exports = ManagementDashboard;
