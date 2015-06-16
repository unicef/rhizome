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

  return (
    <tr className={i % 2 === 0 ? 'even' : 'odd'} key={campaign.id}>
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
  mixins : [Reflux.connect(require('stores/NavigationStore'))],

  getInitialState : function () {
    return {
      visibleCampaigns : 6,
      visibleUploads   : 5
    };
  },

  render : function () {
    var campaigns = _(this.state.campaigns)
      .sortBy('start_date')
      .takeRight(this.state.visibleCampaigns)
      .map(_campaignRow)
      .value();

    var uploads = _(this.state.uploads)
      .take(this.state.visibleUploads)
      .map(_uploadRow)
      .value();

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
                      <a href="/datapoints/campaigns/">see all campaigns</a>
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
              <h2>Recent CSV Uploads</h2>
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
