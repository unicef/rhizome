'use strict'
var _ = require('lodash')
var api = require('data/api')
var moment = require('moment')
var React = require('react')
var Reflux = require('reflux')
var ReactJson = require('react-json')
var ReactRouter = require('react-router')
var { Route, Router } = ReactRouter

var SimpleFormStore = require('stores/SimpleFormStore')
var SimpleFormActions = require('actions/SimpleFormActions')
var IndicatorTagDropdownMenu = require('component/IndicatorTagDropdownMenu.jsx')
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx')

var SimpleFormComponent = React.createClass({
  propTypes: {
    objectId: React.PropTypes.number.isRequired,
    contentType: React.PropTypes.string.isRequired,
    componentTitle: React.PropTypes.string.isRequired,
    onClick: React.PropTypes.func,
    smallItemCouldClick: React.PropTypes.bool,
    onSmallItemClick: React.PropTypes.func,
    smallIDCouldClick: React.PropTypes.bool,
    smallIDBaseUrl: React.PropTypes.string
  },

  mixins: [
    Reflux.connect(SimpleFormStore, 'store')
  ],

  getDefaultProps: function () {
    return {
      onClick: _.noop,
      smallItemCouldClick: false,
      onSmallItemClick: _.noop,
      smallIDCouldClick: false,
      smallIDBaseUrl: ''
    }
  },

  getInitialState: function () {
    return {}
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    // FIXME be more specific
    return nextState.store === this.state.store
  },

  componentWillMount: function () {
    // FIXME use data as opposed to hacky control flow here!
    if (this.props.contentType === 'indicator_tag') {
      SimpleFormActions.initIndicatorToTag(this.props.objectId)
    } else if (this.props.contentType === 'indicator_calc') {
      SimpleFormActions.initIndicatorToCalc(this.props.objectId)
    }
  },

  _onClick: function (value) {
    if (this.props.onClick !== null) {
      this.props.onClick.call(this, this.refs.selectBox.getDOMNode().value, value)
    }
  },

  render: function () {
    var self = this
    var contentType = this.props.contentType
    var componentTitle = this.props.componentTitle
    var data = this.state.store.componentData

    var componentDataExists = _.has(data, contentType)

    if (!componentDataExists) {
      return <div>Loading Form Component </div>
    }

    data = this.state.store.componentData[contentType]
    var rowData = data.componentRows
    var dropDownData = data.dropDownData

    var formComponentStyle = {
      border: '1px dashed #000000',
      width: '90%',
      padding: '10px'
    }

    var rowLi = rowData.map(row => {
      let link = this.props.smallIDCouldClick
        ? (
          <a href={this.props.smallIDBaseUrl + row.displayId} target='_blank' className='clickable underline'>
            {row.displayId}
          </a>
        )
        : (<span>{row.displayId}</span>)

      return (
        <li>
          {row.display}
          ({link})
          {this.props.smallItemCouldClick &&
          <span onClick={self.props.onSmallItemClick.bind(row, row.id)} className='fa fa-fw fa-times clickable'></span>}
        </li>
      )
    })

    var componentForm
    if (contentType === 'indicator_tag') {
      componentForm = (
        <div>
          <IndicatorTagDropdownMenu
            tag_tree={dropDownData}
            text='Add Tag'
            sendValue={this.props.onClick}>
          </IndicatorTagDropdownMenu>
        </div>
      )
    } else if (contentType === 'indicator_calc') {
      componentForm = (
        <form>
          <select ref='selectBox'>
            <option value='PART_TO_BE_SUMMED'>PART_TO_BE_SUMMED</option>
            <option value='PART_OF_DIFFERENCE'>PART_OF_DIFFERENCE</option>
            <option value='WHOLE_OF_DIFFERENCE'>WHOLE_OF_DIFFERENCE</option>
            <option value='PART'>PART</option>
            <option value='WHOLE'>WHOLE</option>
            <option value='WHOLE_OF_DIFFERENCE_DENOMINATOR'>WHOLE_OF_DIFFERENCE_DENOMINATOR</option>
          </select>
          <IndicatorDropdownMenu
            text='Add Component'
            indicators={dropDownData}
            sendValue={this._onClick}>
          </IndicatorDropdownMenu>
        </form>
      )
    }

    return <div style={formComponentStyle}>
      <h4> {componentTitle} </h4>
      <br></br>
      <ul>
        {rowLi}
      </ul>
      {componentForm}
    </div>
  }
})

module.exports = SimpleFormComponent
