'use strict';
var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')

var SimpleForm = React.createClass({

  getInitialState : function () {
    return {
      visibleCampaigns : 6,
      visibleUploads   : 5
    };
  },


  render : function () {
    var doc = {
        user: "",
        password: ""
    };

    var settings = {
        form: true,
        fields: { password: {type: 'password'} }
    };

    return (

          <div className="row">
            <div className="small-12 columns">
              <p className="pageWelcome">
                Welcome to UNICEF&rsquo;s Polio Eradication data portal.
              </p>
              <ReactJson value={ doc } settings={ settings }/>,
            </div>
          </div>
    );
  }
});

module.exports = SimpleForm;
