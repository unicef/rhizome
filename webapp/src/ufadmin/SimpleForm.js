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


var SimpleFormComponent = React.createClass({
  mixins: [
    Reflux.connect(SimpleFormStore, 'store'),
    // ReactRouter.State ,
  ],

  propTypes: {
    objectId : React.PropTypes.number.isRequired,
    contentType : React.PropTypes.string.isRequired,
    componentTitle : React.PropTypes.string.isRequired,
    onClick : React.PropTypes.isRequired,
    rowData : React.PropTypes.array,
    },

  getInitialState : function(){
    return {
        modalIsOpen: false,
      }
  },

  componentWillMount: function () {
    console.log('=== MOUNTING ==')
    // SimpleFormActions.initialize();
  },

  render : function(){

    var rowData = this.props.rowData;
    if (!rowData){
      return <div>Loading Form Component </div>
    }

    var contentType = this.props.contentType;
    var componentTitle = this.props.componentTitle;
    var formComponentStyle = {
      border: '1px dashed #000000',
      width: '90%',
      padding: '10px',
    };

    var rowLi = []
    _.forEach(rowData, function(row) {
        rowLi.push(<li>{row.display} ({row.id}) </li>)
    });

    return <div style={formComponentStyle}>
      <h4> {componentTitle} </h4>
        <br></br>
        <ul>
          {rowLi}
        </ul>
      <span
        onClick={this.props.onClick}
        className="fa fa-plus fa-large"
      > add new {contentType}!
      </span>
    </div>;
  }

})

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
    SimpleFormActions.initialize(this.props.params.id)
	},

  logSomething : function() {
    console.log('logSomething')
  },

  getSubComponentData : function() {
    SimpleFormActions.getTagForIndicator();
  },

  render : function () {
    var tag_form_data, calc_form_data = {};

    // console.log('this dot props: ', this.props)
    // console.log('this dot state : ', this.state)

    var indicatorId  = this.props.params.id
    var indicatorObject  = this.state.store.indicatorObject

    var indicatorTagList  = _.map(this.state.store.indicatorTagList, function(row) {
        var rowCleaned = {'id': row.id, 'display': row.indicator_tag__tag_name}
        return rowCleaned
    });

    var indicatorCalcList  = _.map(this.state.store.indicatorCalcList, function(row) {
        var rowCleaned = {'id': row.indicator_component_id, 'display': row.indicator_component__short_name}
        return rowCleaned
    });

    // CASE 1 ->  There is an id in the url but the request is still pending //
    if (indicatorId && !indicatorObject){
      return <div>'LOADING'</div>
    }

    // CASE 2 -> no object_id: load only the base form for this model
    // render a create form with none of the additional components //
    if (!indicatorId){
        var form_welcome_text = 'Create a New Indicator Below'
        base_form_data = {
            name: "",
            short_name: ''
        };
    }

    // CASE 3 -> He have the object - render the component forms for indicator
    else {
        var form_welcome_text = 'Update Indicator: ' + indicatorObject.short_name
        var base_form_data = {name: indicatorObject.name, short_name: indicatorObject.short_name}
        var calc_form_data = {};
    };

    var base_form_settings = {form: true}
    var base_form = <div>
        <p className="pageWelcome"> {form_welcome_text} </p>
        <ReactJson value={ base_form_data } settings={base_form_settings}/>,
      </div>;

    return (
      <div className="row">
        <div className="small-8 columns">
          {base_form}
        </div>
        <div className="small-4 columns">
          <SimpleFormComponent
              objectId={indicatorId}
              contentType='indicator_tag'
              componentTitle="Tags and Dashboards"
              rowData={indicatorTagList}
              onClick={this.logSomething}
            >
          </SimpleFormComponent>
          <br></br>
            <SimpleFormComponent
                objectId={indicatorId}
                contentType='indicator_component'
                componentTitle="Component Indicators"
                rowData={indicatorCalcList}
                onClick={this.logSomething}
              >
            </SimpleFormComponent>
          </div>
      </div>
    );
  }
});

module.exports = SimpleForm;
