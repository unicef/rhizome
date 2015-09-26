'use strict';
var _      = require('lodash');
var api = require('data/api');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var ReactRouter = require('react-router')
var { Route, Router} = ReactRouter;

var SimpleFormStore = require('stores/SimpleFormStore');
var SimpleFormActions = require('actions/SimpleFormActions');
var IndicatorTagDropdownMenu = require('component/IndicatorTagDropdownMenu.jsx');

var SimpleFormComponent = React.createClass({
  propTypes: {
    objectId : React.PropTypes.number.isRequired,
    contentType : React.PropTypes.string.isRequired,
    componentTitle : React.PropTypes.string.isRequired,
    onClick : React.PropTypes.isRequired,
    getRowData : React.PropTypes.func.isRequired,
    getDropDownData : React.PropTypes.isRequired,
    },

  mixins: [
    Reflux.connect(SimpleFormStore, 'store'),
  ],

  getDefaultProps : function () {
    return {
      onClick    : _.noop,
    };
  },

  getInitialState : function(){
    return {
        rowData: [],
        dropDownData: []
      }
  },

  componentWillMount: function () {
    // shoudld be.. this.props.getRowData //
    SimpleFormActions.initIndicatorToTag(this.props.objectId)
    // shoudld be.. this.props.getDropDownData //
    // SimpleFormActions.getTagForIndicator(this.props.objectId)
  },

  render : function(){

    // console.log('this dot props: ', this.props)
    console.log('this dot state : ', this.state)

    var contentType = this.props.contentType;
    var componentTitle = this.props.componentTitle;
    var data =  this.state.store.componentData //[contentType]

    if (!data){
      return <div>Loading Form Component </div>
    }

    var rowData = data[contentType].componentRows
    var dropDownData = data[contentType].dropDownData
    console.log('data:', data)
    console.log('contentType', contentType)
    console.log('rowData:', rowData)


    var formComponentStyle = {
      border: '1px dashed #000000',
      width: '90%',
      padding: '10px',
    };

    var rowLi = []
    _.forEach(rowData, function(row) {
        rowLi.push(<li>{row.display} ({row.id}) </li>)
    });

    var componentForm = ''
    if (contentType == 'indicator_tag'){

      var componentForm = <div>
        <IndicatorTagDropdownMenu
          tag_tree={dropDownData}
          text='Add Tag'
          sendValue = {this.props.onClick}>
        </IndicatorTagDropdownMenu>
      </div>
    };

    return <div style={formComponentStyle}>
      <h4> {componentTitle} </h4>
        <br></br>
        <ul>
          {rowLi}
        </ul>
          {componentForm}
    </div>;
  }
})

module.exports = SimpleFormComponent;
