'use strict';

var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux/src');

var NavigationStore = require('stores/NavigationStore');

function _dashboardSelect(dashboards) {
  if (_.isEmpty(dashboards)) {
    return null;
  }

  // FIXME: This should render a dropdown with all other available dashboards
  return (
    <a href={'/datapoints/' + dashboards[0].path}>
      {dashboards[0].title}
    </a>
  );
}

function _campaignRow(campaign, i) {
  var country;
  var district;
  var others = [];

  _.each(campaign.dashboards, function (d) {
    switch (d.title) {
      case 'Management Dashboard':
        country = (<a href={'/datapoints/' + d.path}>Country</a>);
        break;
      case 'District Dashboard':
        district = (<a href={'/datapoints/' + d.path}>District</a>);
        break;
      default:
        if (!d.hasOwnProperty('default_office_id') || d.default_office_id === campaign.office_id) {
          others.push(d);
        }
        break;
    }
  });

  var cls = i % 2 === 0 ? 'even' : 'odd';

  return (
    <tr className={cls} key={campaign.id}>
      <td>{campaign.title}</td>
      <td>{country}</td>
      <td>{district}</td>
      <td>{_dashboardSelect(others)}</td>
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
  mixins : [
    Reflux.connect(NavigationStore)
  ],

  getInitialState : function () {
    return {
      visibleCampaigns : 6,
      visibleUploads   : 5
    };
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

    // data entry section, according to permissions
    if (NavigationStore.userHasPermission('upload_csv') || NavigationStore.userHasPermission('data_entry_form')) {

      var csv_upload_button = '';
      if (NavigationStore.userHasPermission('upload_csv')) {
        csv_upload_button = (
                <a className="small button" href="/source_data/file_upload">
                  <i className="fa fa-upload"></i>&emsp;Upload data
                </a>
              );
      }

      var data_entry_button = '';
      if (NavigationStore.userHasPermission('data_entry_form')) {
        data_entry_button = (
                <a className="small button" href="/datapoints/entry">
                  <i className="fa fa-table"></i>&emsp;Data Entry Form
                </a>
              );
      }

      var uploads = <tr><td>No uploads yet.</td></tr>;
      if (this.state.uploads && this.state.uploads.length > 0) {
        uploads = this.state.uploads.map(_uploadRow);
      }

      var dataEntry = (
          <div className="row">
            <div className="medium-4 columns">
              <h2>Enter Data</h2>
              {data_entry_button}
              &emsp;
              {csv_upload_button}
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
        );

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

          {dataEntry}

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
