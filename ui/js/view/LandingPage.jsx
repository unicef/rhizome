'use strict';

var _      = require('lodash');
var moment = require('moment');
var React  = require('react');

var api = require('data/api');

function _loadCampaigns(campaigns, offices) {
  var recent = _(campaigns)
    .each(function (campaign) {
      campaign.office = offices[campaign.office_id];
    })
    .sortBy('start_date')
    .takeRight(6)
    .reverse()
    .value();

  // jshint validthis: true
  this.setState({ campaigns : recent });
}

function _campaignRow(campaign, i) {
  var m        = moment(campaign.start_date, 'YYYY-MM-DD');
  var date     = m.format('MMMM YYYY');
  var datePath = m.format('YYYY/MM');

  return (
    <tr className={i % 2 === 0 ? 'even' : 'odd'} key={campaign.id}>
      <td>{campaign.office.name}: {date}</td>
      <td>
        <a href={'/datapoints/management-dashboard/' + campaign.office + '/' + datePath}>
          Country
        </a>
      </td>
      <td>
        <a href={'/datapoints/district/' + campaign.office + '/' + datePath}>
          District
        </a>
      </td>
      <td></td>
    </tr>
  );
}

function _uploadRow(upload) {
  return (
    <tr key={upload.id}>
      <th>{upload.user}</th>
      <td>{upload.file}</td>
      <td>{upload.status}</td>
    </tr>
  );
}

module.exports = React.createClass({
  getInitialState : function () {
    return {
      campaigns : [],
      uploads   : []
    };
  },

  componentWillMount : function () {
    Promise.all([
        api.campaign().then(_.property('objects')),
        api.office().then(function (d) {
          return _.indexBy(d.objects, 'id');
        })
      ])
      .then(_.spread(_loadCampaigns.bind(this)));
  },

  render : function () {
    var campaigns = this.state.campaigns.map(_campaignRow);
    var uploads   = this.state.uploads.map(_uploadRow);

    return (
      <div className="row">
        <div className="medium-9 columns">

          <div className="row">
            <div className="small-12 columns">
              <p>
                Welcome to UNICEF&rsquo;s Polio Eradication data portal.
              </p>

              <h2>Recent Campaigns</h2>
              <table>{campaigns}</table>
              <a href="">see all campaigns</a>
            </div>
          </div>

          <div className="row">
            <div className="medium-4 columns">
              <h2>Enter Data</h2>
              <a className="small button" href="/datapoints/entry">
                <i className="fa fa-table"></i>&emsp;Data Entry Form
              </a>&emsp;<a className="small button" href="/source_data/file_upload">
                <i className="fa fa-upload"></i>&emsp;Upload data
              </a>
            </div>
            <div className="medium-8 columns">
              <h2>Recent CSV Uploads</h2>
              <table>{uploads}</table>
              <a href="">see all uploads</a>
            </div>
          </div>

        </div>

        <div className="medium-3 columns">
          <h2>About</h2>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed placerat mi
            nec odio egestas bibendum. Praesent tincidunt et neque in vestibulum.
            Quisque eget enim ipsum.&ensp;<a href="/about" style={{whiteSpace: "nowrap"}}>
            <i className="fa fa-info-circle"></i> Learn more
            </a>
          </p>
        </div>
      </div>
    );
  }
});
