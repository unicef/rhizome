import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

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

  cellId: 'edit_id_' + randomHash(),

  propTypes: {
    item: React.PropTypes.object
  },

  componentWillMount: function () {
    this.previousValue = this.props.item.value || null
  },

  validateValue: function (val) {
    if (_.isString(val)) { // string
      if (val.length === 0) { val = null }
    } else if (_.isNaN(val)) { // NaN
      val = null
    }

    // custom validation
    if (this.props.item.validate) {
      val = this.props.item.validate(val)
    }

    // update value
    return val
  },

  formatted: function () {
    if (this.props.item.value === undefined || this.props.item.value === null) {
      return ''
    } else {
      // format according to attached method if it exists
      return this.props.item.format ? this.props.item.format(this.props.item.value) : this.props.item.value
    }
  },

  missing: function () {
    return _.isNull(this.props.item.value)
  },

  _toggleEditing: function (editing) {
    if (this.props.item.isEditable === true) {
      this.isEditing = editing !== undefined ? editing : !this.isEditing
      this.forceUpdate()

      // set focus on input
      if (this.isEditing === true) {
        CellActions.focusInput(this.cellId)
      }
    }
  },
  _focus: function () {
    var dom = document.getElementById(this.cellId)
    dom.value = this.props.item.value
    dom.select()
  },

  _keuUp: function (event) {
    if (event.keyCode === 13) {
      this._submit(event)
    }
  },

  _judgeValue: function (value) {
    if (!Number(value)) {
      this.hasError = true
    } else {
      this.hasError = false
    }
  },

  _submit: function (event) {
    if (this.props.item.isEditable) {
      if (this.isSaving === false) {
        // only perform the save if value has changed
        let value = event.target.value
        this._judgeValue(value)
        if (value !== this.previousValue) {
          this.isSaving = true
          var passed = true

          let validatedValue = this.validateValue(value)
          // validation
          if (validatedValue !== null) {
            value = validatedValue
          } else {
            // did not pass validation
            this.hasError = true
            this.isSaving = false
            passed = false
            this._toggleEditing(true)
          }

          // submit value for saving
          if (passed === true && this.props.item.buildSubmitPromise !== undefined) {
            // TODO: validation of value
            var promise = this.props.item.buildSubmitPromise(value)
            promise.then(response => {
              // fulfilled
              if (this.props.item.withResponse) {
                this.props.item.withResponse(response)
              }
              // done saving
              this.previousValue = value
              this.props.item.value = value
              this.isSaving = false
              this.isEditing = false
              this._toggleEditing(false)
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

              // done saving do not update value
              this.isSaving = false
            })
          }
        }

        this._toggleEditing(false)
      }
    }
  },

  render: function () {
    let inputValue = this.formatted()
    let input = (<input type='textfield' onFocus={this._focus} className='editControl' onBlur={this._submit} onKeyUp={this._keuUp} id={this.cellId} />)

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
        <div onClick={this._toggleEditing.bind(this, true)} className='displayValue'>
          {inputValue}
        </div>
        {itemInput}
      </td>
    )
  }
})

export default Cell
