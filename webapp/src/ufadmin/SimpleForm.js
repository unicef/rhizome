'use strict';
var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var ReactRouter = require('react-router')
var { Route, Router} = ReactRouter;

var SimpleFormStore = require('stores/SimpleFormStore');
var SimpleFormActions = require('actions/SimpleFormActions');
var SimpleFormComponent = require('./SimpleFormComponent');


var SimpleForm = React.createClass({
  mixins: [
    Reflux.connect(SimpleFormStore, 'store'),
  ],

  contextTypes: {
    router: React.PropTypes.func
  },

  getInitialState : function () {
    return {};
  },

  componentWillMount: function() {
      SimpleFormActions.initialize(this.props.params.id,this.props.params.contentType)
	},

  componentWillReceiveProps: function(nextProps) {
    SimpleFormActions.initialize(nextProps.params.id,nextProps.params.contentType)
  },

  addTagToIndicator : function(e) {
    var tag_id = e
    SimpleFormActions.addTagToIndicator(this.props.params.id, e)
  },

  componentWillUpdate : function (nextProps, nextState) {
      if (nextProps.params != this.props.params) {
        return;
      }
    },
  onSubmit: function( e ){
    e.preventDefault();
    var data = this.refs.form_data.getValue();
    SimpleFormActions.baseFormSave(this.props.params.id,this.props.params.contentType,data)
  },

  render : function () {
    var tag_form_data, calc_form_data = {};

    // console.log('this dot props: ', this.props)
    // console.log('this dot state : ', this.state)

    var objectId  = this.props.params.id
    var contentType = this.props.params.contentType
    var dataObject  = this.state.store.dataObject
    var formData = this.state.store.formData;
    var formSettings = {'form': true, fields: {'tag_name': { type: 'string'}} } // this.state.store.form_settings;

    // There is an id in the url but the request is still pending //
    if (objectId && !dataObject){
      return <div>Loading MetaData Manager</div>
    }

    var base_form = <div>
        <p className="pageWelcome"> Welcome! </p>
        <ReactJson value={formData} settings={formSettings} ref="form_data" />,
        <button className="tiny" style={{textAlign: "right"}} onClick={ this.onSubmit }>Save</button>
      </div>;

    var sub_form_list = '';
    if (contentType == 'indicator' && objectId > 0) {
        var sub_form_list =<div><SimpleFormComponent
            objectId={objectId}
            contentType={contentType}
            componentTitle="componentTitle"
            onClick={this.addTagToIndicator}
          >
        </SimpleFormComponent>
          <br></br>
        <SimpleFormComponent
            objectId={objectId}
            contentType='indicator_calc'
            componentTitle="componentTitle"
            onClick={this.addTagToIndicator}
          >
        </SimpleFormComponent></div>
    }

    return (
      <div className="row">
        <div className="small-8 columns">
          {base_form}
        </div>
        <div className="small-4 columns">
          {sub_form_list}
        </div>
      </div>
    );
  }
});

module.exports = SimpleForm;
