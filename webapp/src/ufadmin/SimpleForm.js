'use strict';
var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var page  = require('page');
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
    return {
        objectId: -1,
        saveSuccess: false
    };
  },

  componentWillMount: function() {
      this.setState({'objectId':this.props.params.id})
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
      if (nextState.store.dataObject != this.state.store.dataObject){
        return;
      }
    },
  onSubmit: function( e ){
    e.preventDefault();
    var data = this.refs.form_data.getValue();
    SimpleFormActions.baseFormSave(this.props.params.id,this.props.params.contentType,data)
    // when creating new //
    console.log('setting state after save')
    this.setState({'objectId':this.state.store.objectId, 'saveSuccess':true})

  },

  render : function () {
    var tag_form_data, calc_form_data = {};

    // console.log('this dot props: ', this.props)
    console.log('this dot state : ', this.state)

    var objectId  = this.state.objectId
    var contentType = this.props.params.contentType
    var dataObject  = this.state.store.dataObject
    var formData = this.state.store.formData;

    // TODO -> pull this from the DB
    var formSettings = {'form': true, fields: {'tag_name': { type: 'string', editing: false} }}

    // There is an id in the url but the request is still pending //
    if (objectId && !dataObject){
      return <div>Loading MetaData Manager</div>
    }

    if (dataObject){
      // match up the data from the dataObject
      for (var key in formData) {
        if (dataObject.hasOwnProperty(key)) {
          formData[key] = dataObject[key];
        }
      }
    }

    // this is the basic form used for all content types
    var base_form = <div>
        <p className="pageWelcome"> Welcome! </p>
        <h5>id: {this.state.store.objectId} </h5>
        <br></br>
        <ReactJson value={formData} settings={formSettings} ref="form_data" />,
        <button className="tiny" style={{textAlign: "right"}} onClick={ this.onSubmit }>Save</button>
      </div>;

    var base_form_success = ''
    if (this.state.saveSuccess){
      var base_form_success = <i className="fa fa-check"> saved successfully </i>
    }
    var sub_form_list = '';

    if (contentType == 'indicator') {
        var sub_form_list =<div><SimpleFormComponent
            objectId={objectId}
            contentType={'indicator_tag'}
            componentTitle="Add Tags to Indicators"
            onClick={this.addTagToIndicator}
          >
        </SimpleFormComponent>
          <br></br>
        <SimpleFormComponent
            objectId={objectId}
            contentType='indicator_calc'
            componentTitle="Add Calculations to Indicators"
            onClick={this.addTagToIndicator}
          >
        </SimpleFormComponent></div>
    }

    return (
      <div className="row">
        <div className="small-8 columns">
          {base_form}
          <div>{base_form_success}</div>
        </div>
        <div className="small-4 columns">
          {sub_form_list}
        </div>
      </div>
    );
  }
});

module.exports = SimpleForm;
