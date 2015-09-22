'use strict';
var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var SimpleFormStore = require('stores/SimpleFormStore');
var SimpleFormActions = require('actions/SimpleFormActions');

var SimpleForm = React.createClass({
  mixins: [
    Reflux.connect(SimpleFormStore)
  ],

  getInitialState : function () {
    return {
      visibleCampaigns : 6,
      visibleUploads   : 3
    };
  },

  componentWillMount: function() {
		// init store, passing indicator id if present
		SimpleFormActions.init(164);
	},

  render : function () {
    var doc = {
        name: "",
        short_name: ""
    };

    var settings = {
        form: true,
        fields: { password: {type: 'password'} }
    };

    return (

          <div className="row">
            <div className="small-8s columns">
              <p className="pageWelcome">
                Create an Indicator Below
              </p>
              <form>
                <ReactJson value={ doc } settings={ settings }/>,

                  </form>
            </div>
          </div>
    );
  }
});

module.exports = SimpleForm;
