'use strict';
var _      = require('lodash');
var api = require('data/api');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var ReactRouter = require('react-router')
var { Route, Router} = ReactRouter;

var SimpleFormModal = require('./SimpleFormModal');
var IndicatorTagDropdownMenu = require('component/IndicatorTagDropdownMenu.jsx');

var SimpleFormComponent = React.createClass({
  propTypes: {
    objectId : React.PropTypes.number.isRequired,
    contentType : React.PropTypes.string.isRequired,
    componentTitle : React.PropTypes.string.isRequired,
    onClick : React.PropTypes.isRequired,
    rowData : React.PropTypes.array,
    getDropDownData : React.PropTypes.isRequired,
    },

  getDefaultProps : function () {
    return {
      onClick    : _.noop,
    };
  },

  getInitialState : function(){
    return {
        modalIsOpen: false,
        dropDownData: []
      }
  },

  componentWillMount: function () {
    var self = this;
    // shoudld be.. this.props.getDropDownData //
    api.tagTree().then(function(response){
        self.setState({dropDownData: response.objects})
        console.log('taG response respone',response.objects)
    })
  },

  render : function(){

    console.log('this dot props: ', this.props)
    console.log('this dot state : ', this.state)

    var contentType = this.props.contentType;
    var componentTitle = this.props.componentTitle;
    var rowData = this.props.rowData;

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

    var modalForm = ''
    if (contentType == 'indicator_tag'){
      var tagTree = this.state.dropDownData
      var modalForm = <div>
        <IndicatorTagDropdownMenu
          tag_tree={tagTree}
          text='Add Tag'
          sendValue = {this.props.onClick}>
        </IndicatorTagDropdownMenu>
        <ReactJson value={ {'hello':'','world':''} } settings={{'form': 'true'}}/>
      </div>
    };

    return <div style={formComponentStyle}>
      <h4> {componentTitle} </h4>
        <br></br>
        <ul>
          {rowLi}
        </ul>
      <SimpleFormModal
        modalForm={modalForm}
        onClick={this.props.onClick}
        contentType={contentType}
        >
      </SimpleFormModal>

    </div>;
  }
})

module.exports = SimpleFormComponent;
