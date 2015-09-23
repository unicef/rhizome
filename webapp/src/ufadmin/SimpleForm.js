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

    // console.log('this dot props: ', this.props)
    // console.log('this dot state : ', this.state)

    var indicatorId  = this.props.params.id
    var indicatorObject  = this.state.store.indicatorObject

    if (indicatorId && !indicatorObject){
      return <div>'LOADING'</div>
    }

    if (!indicatorId){
    // render a create form with none of the additional components //
        var form_welcome_text = 'Create a New Indicator Below'
        base_form_data = {
            name: "",
            short_name: ''
        };
        var tag_form_data = {};
        var bound_form_data = {};
        var calc_form_data = {};
    }
    else {
        var form_welcome_text = 'Update Indicator: ' + indicatorObject.short_name
        var base_form_data = {name: indicatorObject.name, short_name: indicatorObject.short_name}
        var tag_form_data = {};
        var bound_form_data = {};
        var calc_form_data = {};
    };

    var base_form_settings = {
        form: true,
    };

    var base_form = <div>
        <p className="pageWelcome"> {form_welcome_text} </p>
        <ReactJson value={ base_form_data } settings={ base_form_settings }/>,
      </div>
;

    return (
      <div className="row">
        <div className="small-8 columns">
          {base_form}
        </div>
      </div>
    );
  }
});

module.exports = SimpleForm;
