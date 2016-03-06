import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import Layer from 'react-layer'
import Tooltip from 'components/molecules/Tooltip.jsx'
import moment from 'moment'
import numeral from 'numeral'

import TableEditableCellStore from 'stores/TableEditableCellStore'
import TableEditableCellActions from 'actions/TableEditableCellActions'
import randomHash from 'utilities/randomHash'

var Cell = React.createClass({
  mixins: [Reflux.connect(TableEditableCellStore)],

  previousValue: null, // save the previous value to compare with edited value
  isSaving: false, // whether the cell is in the process of saving right now
  isEditable: false, // whether the cell is editable
  isEditing: false, // whether the cell is currently being edited
  hasError: false,
  displayValue: null,
  tip: null,

  cellId: 'edit_id_' + randomHash(),

  propTypes: {
    name: React.PropTypes.string,
    schema: React.PropTypes.string,
    field: React.PropTypes.string,
    value: React.PropTypes.string,
    isEditable: React.PropTypes.bool,
    validateValue: React.PropTypes.func,
    buildSubmitPromise: React.PropTypes.func,
    classes: React.PropTypes.string,
    format: React.PropTypes.func,
    tooltip: React.PropTypes.string,
    type: React.PropTypes.string
  },

  componentWillMount: function () {
    if (this.props.value) {
      this.previousValue = this.props.value.toString()
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
    if (this.props.validate) {
      val = this.props.validate(val)
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
      return this.props.format ? this.props.format(this.displayValue) : this.displayValue
    }
  },

  missing: function () {
    return _.isNull(this.displayValue)
  },



  _keyUp: function (event) {
    if (event.keyCode === 13) {
      this._submit(event)
    }
  },

  _submit: function (event) {
    TableEditableCellActions.updateValue(event)
    if (this.props.isEditable) {
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
          if (passed === true && this.props.buildSubmitPromise !== undefined) {
            console.log('this.state', this.state)
            console.log('this.props', this.props)
            var promise = this.props.buildSubmitPromise(value)
            promise.then(response => {
              // done saving
              this.previousValue = value
              this.props.value = value
              this.displayValue = value
              this.isSaving = false
              this.hasError = false
              this.isEditing = false
              this._toggleEditing(false)

              if (this.props.withResponse) {
                this.props.withResponse(response)
              }
            }, error => {
              // or rejected
              if (this.props.withError) {
                this.props.withError(error)
              } else {
                console.log('Error', error)
              }

              // set to previous value
              this.hasError = true
              this.props.value = this.previousValue
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
    let message = _.isNull(this.props.value) ? 'Missing value' : this.props.value

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

  _toggleEditing: function (editing) {
    if (this.props.isEditable === true) {
      this.isEditing = editing !== undefined ? editing : !this.isEditing
      this.forceUpdate()

      // set focus on input
      if (this.isEditing === true) {
        CellActions.focusInput(this.cellId, this.displayValue)
      }
    }
  },


  render: function () {
    console.log('I changed state')
    let inEditMode = this.props.isEditable && this.state.editMode

    let display_value = !inEditMode ? this.formatted() : ''
    let input_field = inEditMode ? <input type='textfield' className='ditControl' onBlur={this._submit} onKeyUp={this._keyUp} id={this.cellId} /> : ''
    let spinner = this.props.isSaving ? <i className='fa fa-spinner fa-spin saving-icon'></i> : ''

    let class_string = ''
    class_string += this.props.class ? this.props.class : ''
    class_string += this.props.isEditable ? 'editable ' : ''
    class_string += this.state.editMode ? 'editing ' : ''
    class_string += this.missing() ? 'missing ' : ''
    class_string += this.isSaving ? 'saving ' : ''
    class_string += this.hasError ? 'error ' : ''

    return (
      <td onClick={TableEditableCellActions.toggleEditMode.bind(this, this)}
        className={class_string}
        colSpan={this.props.colspan}
        onMouseOver={this._mouseOver}
        onMouseOut={this._mouseOut}>
          {spinner}
          <span className='displayValue'>{display_value}</span>
          {input_field}
      </td>
    )
  }
})

export default Cell
