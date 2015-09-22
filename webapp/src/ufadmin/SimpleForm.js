'use strict';
var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var SimpleFormStore = require('stores/SimpleFormStore');
var SimpleFormActions = require('actions/SimpleFormActions');
var ReactRouter = require('react-router')
var { Route, Router} = ReactRouter;


var SimpleForm = React.createClass({
  mixins: [
    Reflux.connect(SimpleFormStore, 'store'),
    // ReactRouter.State ,
  ],

  contextTypes: {
    router: React.PropTypes.func
  },

  getInitialState : function () {
    return {
    };
  },

  componentWillMount: function() {
    console.log('query indicators for id: ',this.props.params.id)
    SimpleFormActions.initialize(this.props.params.id)
	},

  render : function () {

    console.log('this dot props: ', this.props)
    console.log('this dot state dot store : ', this.state.store)

    var q_params = this.context.router.getCurrentParams()

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
        <div className="small-8 columns">
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
