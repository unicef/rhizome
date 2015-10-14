'use strict';
var _      = require('lodash');
var moment = require('moment');
var api = require('data/api');
var React  = require('react');
var page  = require('page');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var ReactRouter = require('react-router')
var { Route, Router} = ReactRouter;

var SimpleFormStore = require('stores/SimpleFormStore');
var SimpleFormActions = require('actions/SimpleFormActions');
var SimpleFormComponent = require('./SimpleFormComponent');
var IndicatorTagDropdownMenu = require('component/IndicatorTagDropdownMenu.jsx');


var SimpleForm = React.createClass({
  mixins: [
    Reflux.connect(SimpleFormStore, 'store'),
  ],

  contextTypes: {
    router: React.PropTypes.func
  },

  getInitialState : function () {
    return {
        objectId: null,
        saveSuccess: false,
        extraFormData: {},
        tagTree: [],
    };
  },

  componentWillMount: function() {
      var self = this;
      this.setState({'objectId':this.props.params.id})
      SimpleFormActions.initialize(this.props.params.id,this.props.params.contentType)

      // Hack alert.. FIXME ( this is for the parent_tag_dropdown) //
      if (this.props.params.contentType == 'indicator_tag'){
        api.tagTree({},null,{'cache-control': 'no-cache'}).then(function(response){
          self.setState({'tagTree':response.objects})
        })
      }
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
      if (nextState.extraFormData != this.state.extraFormData){
        return;
      }
    },
  onSubmit: function( e ){
    e.preventDefault();
    var data = this.refs.form_data.getValue();

    // if there is any data in the react-json form add it here //
    for (var key in this.state.extraFormData) {
        data[key] = this.state.extraFormData[key];
    }

    SimpleFormActions.baseFormSave(this.props.params.id,this.props.params.contentType,data)
    // when creating new //
    this.setState({'objectId':this.state.store.objectId, 'saveSuccess':true})
  },

  setParentTag: function ( e ) {
      var extraFormData = { 'parent_tag_id': e }
      console.log(extraFormData)
      this.setState({'extraFormData':extraFormData})
  },

  render : function () {
    var tag_form_data, calc_form_data = {};

    var objectId  = this.state.objectId
    var contentType = this.props.params.contentType
    var dataObject  = this.state.store.dataObject
    var formData = this.state.store.formData;

    // TODO -> pull this from the DB
    var formSettings = {'form': true, fields: {'tag_name': { type: 'string', editing: false} }}

    if (objectId && !dataObject){
      if (this.state.store.loading) {
        return <div>Loading MetaData Manager</div>
      } else {
        return (
          <div>Error. There is no data received.</div>
        )
      }
    }

    if (dataObject){
      // match up the data from the dataObject
      for (var key in formData) {
        if (dataObject.hasOwnProperty(key)) {
          formData[key] = dataObject[key];
        }
      }
    }

    var additionalFormComponents;
    if (contentType === 'indicator_tag' && dataObject) {
      var selected =  this.state.extraFormData['parent_tag_id'] || dataObject.parent_tag__tag_name || 'No Parent'
      var tagTree = this.state.tagTree

      additionalFormComponents = (
        <div>
          <p>{`Parent Tag: ${selected}`}</p>
          <br></br>
          <IndicatorTagDropdownMenu
            tag_tree={tagTree}
            text='Parent tag'
            sendValue={ this.setParentTag }
          >
          </IndicatorTagDropdownMenu>
        </div>
      )
    }
    if (contentType === 'indicator') {
      additionalFormComponents = ''
    }

    // this is the basic form used for all content types
    var base_form = (
      <div>
        <p className="pageWelcome"> Welcome! </p>
        <h5>id: {this.state.store.objectId} </h5>
        <br></br>
        <ReactJson value={formData} settings={formSettings} ref="form_data" />
        {additionalFormComponents}
        <br></br>
        <button className="tiny" style={{textAlign: "right"}} onClick={ this.onSubmit }>Save</button>
      </div>);

    var baseFormSuccess = ''
    if (this.state.saveSuccess){
      var baseFormSuccess = <i className="fa fa-check"> saved successfully </i>
    }

    var subFormList;

    if (contentType == 'indicator') {
        subFormList = (
          <div>
            <SimpleFormComponent
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
            </SimpleFormComponent>
          </div>
        )
    }

    return (
      <div className="row">
        <div className="small-8 columns">
          {base_form}
          <div>{baseFormSuccess}</div>
        </div>
        <div className="small-4 columns">
          {subFormList}
        </div>
      </div>
    );
  }
});

module.exports = SimpleForm;
