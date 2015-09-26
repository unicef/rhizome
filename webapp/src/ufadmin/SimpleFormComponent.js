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
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');

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
    if (this.props.contentType == 'indicator_tag'){
      SimpleFormActions.initIndicatorToTag(this.props.objectId)
    }
    else if (this.props.contentType == 'indicator_calc'){
      console.log('InitIndicatorToCalc...')
      SimpleFormActions.initIndicatorToCalc(this.props.objectId)
    }

    // shoudld be.. this.props.getData //
  },

  render : function(){

    // console.log('this dot props: ', this.props)
    // console.log('this dot state : ', this.state)

    var contentType = this.props.contentType;
    var componentTitle = this.props.componentTitle;
    var data =  this.state.store.componentData

    var compnent_data_exists = _.has(data, contentType);

    if (!compnent_data_exists){
      return <div>Loading Form Component </div>
    }

    var data =  this.state.store.componentData[contentType]

    var rowData = data.componentRows
    var dropDownData = data.dropDownData

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
    // fixme.....
    if (contentType == 'indicator_tag'){

      var componentForm = <div>
        <IndicatorTagDropdownMenu
          tag_tree={dropDownData}
          text='Add Tag'
          sendValue = {this.props.onClick}>
        </IndicatorTagDropdownMenu>
      </div>
    }
    else if (contentType == 'indicator_calc'){
      var componentForm = '1'

      var componentForm = <form>
          <IndicatorDropdownMenu
          text='Add Component'
          indicators={dropDownData}
          sendValue={this.props.onClick}>
        </IndicatorDropdownMenu>;
        <select>
          <option value="PART_TO_BE_SUMMED">PART_TO_BE_SUMMED</option>
          <option value="PART_OF_DIFFERENCE">PART_OF_DIFFERENCE</option>
          <option value="WHOLE_OF_DIFFERENCE">WHOLE_OF_DIFFERENCE</option>
          <option value="PART">PART</option>
          <option value="WHOLE">WHOLE</option>
          <option value="WHOLE_OF_DIFFERENCE_DENOMINATOR">WHOLE_OF_DIFFERENCE_DENOMINATOR</option>
        </select>
        <button> Add! </button>
      </form>
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
