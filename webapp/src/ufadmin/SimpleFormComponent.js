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
    var self = this;

    SimpleFormActions.getTagForIndicator(this.props.objectId)
    console.log('=====mounting======')
    var x = this.props.getRowData()
    console.log('===========', x)

    // shoudld be.. this.props.getDropDownData //
    // api.tagTree().then(function(response){
    //     self.setState({dropDownData: response.objects})
    //     console.log('taG response respone',response.objects)
    // })
  },

  render : function(){

    console.log('this dot props: ', this.props)
    console.log('this dot state : ', this.state)

    var contentType = this.props.contentType;
    var componentTitle = this.props.componentTitle;
    var rowData = this.state.store.rowData;

    if (!rowData){
      return <div>Loading Form Component </div>
    }

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
    console.log(contentType)
    if (contentType == 'indicator_tag'){
      var tagTree = this.state.dropDownData

      console.log('HELELLOO')
      var componentForm = <div>
        <IndicatorTagDropdownMenu
          tag_tree={tagTree}
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
