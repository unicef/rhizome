'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');

var api = require('data/api');

var _tableRow = function(row) {
  var path = '/dashboard/'+row.id+'/';
  return (
      <tr>
        <td><a href={path}>{row.title}</a></td>
        <td>{row.description}</td>
        <td>{row.owner_id}</td>
      </tr>
    );
};

var NavigationStore = require('stores/NavigationStore');

module.exports = React.createClass({

  mixins: [
    Reflux.connect(NavigationStore, 'store')
  ],

  render : function () {
    var rows; 
    if (_.isNull(NavigationStore.customDashboards)) {
      rows = <tr><td><i className="fa fa-spinner fa-spin"></i> Loading...</td></tr>;
    } else if (NavigationStore.customDashboards.length > 0) {
      rows = NavigationStore.customDashboards.map(_tableRow);
    } else {
      rows = <tr><td>No custom dashboards created yet.</td></tr>;
    }

    return (
      <div className="row">
        <div className="medium-12 columns">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

});
