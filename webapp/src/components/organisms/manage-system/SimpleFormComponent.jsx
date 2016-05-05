
import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import SimpleFormStore from 'stores/SimpleFormStore'
import SimpleFormActions from 'actions/SimpleFormActions'
import DropdownMenu from 'components/atoms/dropdowns/DropdownMenu.jsx'

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

    console.log('TWHUTHUH: ', this.props.contentType)

    // FIXME use data as opposed to hacky control flow here!
    if (this.props.contentType === 'indicator_tag') {
      SimpleFormActions.initIndicatorToTag(this.props.objectId)
    } else if (this.props.contentType === 'indicator_calc') {
      SimpleFormActions.initIndicatorToCalc(this.props.objectId)
    } else if (this.props.contentType === 'indicator') {
      SimpleFormActions.initTagToIndicator(this.props.objectId)
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
          <DropdownMenu
            items={dropDownData}
            sendValue={this.props.onClick}
            item_plural_name='Indicator Tags'
            text='Add Tag'
            icon='fa-tag'/>
        </div>
      )
    } else if (contentType === 'indicator_calc') {
      componentForm = (
        <form>
          <select ref='selectBox'>
            <option value='PART_TO_BE_SUMMED'>PART_TO_BE_SUMMED</option>
            <option value='PART_OF_DIFFERENCE'>PART_OF_DIFFERENCE</option>
            <option value='WHOLE_OF_DIFFERENCE'>WHOLE_OF_DIFFERENCE</option>
            <option value='NUMERATOR'>NUMERATOR</option>
            <option value='DENOMINATOR'>DENOMINATOR</option>
          </select>
          <DropdownMenu
            items={dropDownData}
            sendValue={this._onClick}
            item_plural_name='Components'
            text='Add Component'/>
        </form>
      )
      console.log("dropDownData: ", dropDownData);
    } else if (contentType === 'indicator') {
        componentForm = (
          <div>
            <DropdownMenu
              items={dropDownData}
              sendValue={this.props.onClick}
              item_plural_name='Indicators'
              text='Add Indicator'/>
          </div>
        )
        //console.log("dropDownData: ", dropDownData);
    }

    return (
      <div style={formComponentStyle}>
        <h4> {componentTitle} </h4>
        <br></br>
        <ul>
          {rowLi}
        </ul>
        {componentForm}
      </div>
    )
  }
})

export default SimpleFormComponent
