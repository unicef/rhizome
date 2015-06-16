'use strict';

var _      = require('lodash');
var moment = require('moment');
var React  = require('react');

var api = require('data/api');

var DashboardStore = require('stores/DashboardStore');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');

function _loadCampaigns(campaigns, offices) {
  var recent = _(campaigns)
    .each(function (campaign, i) {
      campaign.office = offices[campaign.office_id];
    })
    .sortBy('start_date')
    .reverse()
    .value();

  // jshint validthis: true
  this.setState({ campaigns : recent });
}

function _loadDocuments(documents) {
  var recent = _.take(documents, 5);

  this.setState({ uploads : recent });
}

function _includeDashboard(dashboard, office) {
  var slug    = dashboard.slug;
  var offices = dashboard.offices;

  return (slug !== 'management-dashboard' &&
    slug !== 'district' &&
    (_.isEmpty(offices) || offices.indexOf(office) > -1)
  );
}

function _dashboardSelect(dashboards, campaign) {
  if (_.isEmpty(dashboards)) {
    return null;
  }

  var date = moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM');

  // FIXME: This should render a dropdown with all other available dashboards
  return (
    <a href={'/datapoints/' + dashboards[0].slug + '/' + campaign.office.name + '/' + date}>
      {dashboards[0].name}
    </a>
  );
}

function _campaignRow(campaign, i) {
  var m          = moment(campaign.start_date, 'YYYY-MM-DD');
  var date       = m.format('MMMM YYYY');
  var datePath   = m.format('YYYY/MM');
  var dashboards = _(DashboardStore.getAll())
    .filter(_.partial(_includeDashboard, _, campaign.office_id))
    .thru(_.partial(_dashboardSelect, _, campaign))
    .value();

  var cls = i % 2 === 0 ? 'even' : 'odd';

  return (
    <tr className={cls} key={campaign.id}>
      <td>{campaign.office.name}: {date}</td>
      <td>
        <a href={'/datapoints/management-dashboard/' + campaign.office.name + '/' + datePath}>
          Country
        </a>
      </td>
      <td>
        <a href={'/datapoints/district/' + campaign.office.name + '/' + datePath}>
          District
        </a>
      </td>
      <td>{dashboards}</td>
    </tr>
  );
}

function _uploadRow(upload, i) {
  var status = upload.is_processed === 'False' ? 'INCOMPLETE' : 'COMPLETE';
  return (
    <tr className={i % 2 === 0 ? 'odd' : 'even'} key={upload.id}>
      <td>
        <a href={'/source_data/field_mapping/' + upload.id}>{upload.docfile}</a>
      </td>
      <td>{status}</td>
    </tr>
  );
}

module.exports = React.createClass({
  getInitialState : function () {
    return {
      campaigns : [],
      uploads   : [],
      visibleCampaigns: 6
    };
  },

  componentWillMount : function () {
    var getObjects   = _.property('objects');
    var indexObjects = _.partial(_.indexBy, _, 'id');

    Promise.all([
        api.campaign().then(getObjects),
        api.office().then(getObjects).then(indexObjects)
      ])
      .then(_.spread(_loadCampaigns.bind(this)));

    api.document()
      .then(getObjects)
      .then(_loadDocuments.bind(this));
  },

  showAllCampaigns: function(e) {
    this.setState({ visibleCampaigns: Infinity });
    e.preventDefault();
  },

  render : function () {
    var campaigns;
    if (_.isFinite(this.state.visibleCampaigns)) {
       campaigns = _(this.state.campaigns).
                      take(this.state.visibleCampaigns)
                      .map(_campaignRow)
                      .value();
    } else {
       campaigns = this.state.campaigns.map(_campaignRow);
    }

    var uploads = <tr><td>No uploads yet.</td></tr>;
    if (this.state.uploads.length > 0) {
      uploads = this.state.uploads.map(_uploadRow);
    }

    return (
      <div className="row">
        <div className="medium-9 columns">

          <div className="row">
            <div className="small-12 columns">
              <p>
                Welcome to UNICEF&rsquo;s Polio Eradication data portal.
              </p>

              <h2>Recent Campaigns</h2>
              <table>
                <tbody>{campaigns}</tbody>
                <tfoot>
                  <tr>
                    <td className="more" colSpan="4">
                      <a href="#" onClick={this.showAllCampaigns}>see all campaigns</a>
                    </td>
                  </tr>
                </tfoot>
              </table>
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
              <h2>Your Recent CSV Uploads</h2>
              <table>
                <tbody>{uploads}</tbody>
                <tfoot>
                  <tr>
                    <td className="more" colSpan="2">
                      <a href="/source_data/document_index/">see all uploads</a>
                    </td>
                  </tr>
                </tfoot>
              </table>
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
