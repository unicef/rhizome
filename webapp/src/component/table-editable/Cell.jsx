import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import Layer from 'react-layer'
import Tooltip from 'component/Tooltip.jsx'

import CellStore from 'stores/CellStore'
import CellActions from 'actions/CellActions'
import randomHash from 'util/randomHash'

var Cell = React.createClass({
  mixins: [Reflux.connect(CellStore)],

  previousValue: null, // save the previous value to compare with edited value
  isSaving: false, // whether the cell is in the process of saving right now
  isEditable: false, // whether the cell is editable
  isEditing: false, // whether the cell is currently being edited
  hasError: false,
  displayValue: null,
  tip: null,

  cellId: 'edit_id_' + randomHash(),

  propTypes: {
    item: React.PropTypes.object
  },

  componentWillMount: function () {
    if (this.props.item.value) {
      this.previousValue = this.props.item.value.toString()
      this.displayValue = this.previousValue
    }
  },

  validateValue: function (val) {
    var validated = true
    if (_.isString(val)) { // string
      if (val.length === 0) {
        val = null
      } else if (isNaN(Number(val))) {
        val = null
        validated = false
      }
    } else if (_.isNaN(val)) { // NaN
      val = null
      validated = false
    }

    // custom validation
    if (this.props.item.validate) {
      val = this.props.item.validate(val)
      validated = val !== null
    }

    // update value
    return {value: val, validated: validated}
  },

  formatted: function () {
    if (this.displayValue === undefined || this.displayValue === null) {
      return ''
    } else {
      // format according to attached method if it exists
      return this.props.item.format ? this.props.item.format(this.displayValue) : this.displayValue
    }
  },

  missing: function () {
    return _.isNull(this.displayValue)
  },

  _toggleEditing: function (editing) {
    if (this.props.item.isEditable === true) {
      this.isEditing = editing !== undefined ? editing : !this.isEditing
      this.forceUpdate()

      // set focus on input
      if (this.isEditing === true) {
        CellActions.focusInput(this.cellId, this.displayValue)
      }
    }
  },

  _keuUp: function (event) {
    if (event.keyCode === 13) {
      this._submit(event)
    }
  },

  _submit: function (event) {
    if (this.props.item.isEditable) {
      if (this.isSaving === false) {
        // only perform the save if value has changed
        let value = event.target.value
        if (value !== this.previousValue) {
          this.isSaving = true
          var passed = true

          let result = this.validateValue(value)
          // validation

          if (result.validated) {
            value = result.value
          } else {
            // did not pass validation
            this.displayValue = value
            this.hasError = true
            this.isSaving = false
            passed = false
          }

          // submit value for saving
          if (passed === true && this.props.item.buildSubmitPromise !== undefined) {
            var promise = this.props.item.buildSubmitPromise(value)
            promise.then(response => {
              // done saving
              this.previousValue = value
              this.props.item.value = value
              this.displayValue = value
              this.isSaving = false
              this.hasError = false
              this.isEditing = false
              this._toggleEditing(false)

              if (this.props.item.withResponse) {
                this.props.item.withResponse(response)
              }
            }, function (error) {
              // or rejected
              if (this.props.item.withError) {
                this.props.item.withError(error)
              } else {
                console.log('Error', error)
              }

              // set to previous value
              this.hasError = true
              this.props.item.value = this.previousValue
              this.displayValue = this.previousValue
              // done saving do not update value
              this.isSaving = false
              this._toggleEditing(true)
            })
          }
        } else {
          this.displayValue = this.previousValue
          this.hasError = false
        }

        this._toggleEditing(false)
      }
    }
  },

  _mouseOver: function (event) {
    let message = _.isNull(this.props.item.value) ? 'Missing value' : this.props.item.value

    let render = function () {
      return (
        <Tooltip left={event.pageX} top={event.pageY}>
          <div>
            {message}
          </div>
        </Tooltip>
      )
    }

    if (!this.tip) {
      this.tip = new Layer(document.body, render)
    } else {
      this.tip._render = render
    }

    this.tip.render()
  },

  _mouseOut: function () {
    if (this.tip) {
      this.tip.destroy()
      this.tip = null
    }
  },

  render: function () {
    let inputValue = this.formatted()
    let input = (<input type='textfield' className='editControl' onBlur={this._submit} onKeyUp={this._keuUp} id={this.cellId} />)

    let itemInput = this.props.item.isEditable && this.isEditing ? input : ''
    let isEditable = this.props.item.isEditable ? 'editable ' : ''
    let isEditing = this.isEditing ? 'editing ' : ''
    let missing = this.missing() ? 'missing ' : ''
    let saving = this.isSaving ? 'saving ' : ''
    let error = this.hasError ? 'error ' : ''
    let className = isEditable + isEditing + missing + saving + error + this.props.item.class
    let icon = this.props.item.isEditable ? (<i className='fa fa-spinner fa-spin saving-icon'></i>) : ''

    return (
      <td className={className} colSpan={this.props.item.colspan}>
        {icon}
        <div onClick={this._toggleEditing.bind(this, true)} className='displayValue'
          onMouseOver={this._mouseOver} onMouseOut={this._mouseOut}>
          {inputValue}
        </div>
        {itemInput}
      </td>
    )
  }
})

export default Cell
