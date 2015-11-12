'use strict'

import React from 'react'

let LayoutOptions = React.createClass({
  propTypes: {
    values: React.PropTypes.array.isRequired,
    value: React.PropTypes.number.isRequired,
    onChange: React.PropTypes.func.isRequired
  },

  _handleChange (event) {
    this.props.onChange(parseInt(event.target.value, 10))
  },

  render () {
    var self = this

    var radios = this.props.values.map(radio => {
      var radioID = 'layout-option-id-' + radio.value

      return <div href='#' key={radio.value}
                  className={'medium-4 small-12 layout-option ' + (self.props.value === radio.value ? 'active' : 'inactive')}>
                <label htmlFor={radioID}>
                  <h3> {radio.name} </h3>
                  <div className="layout-option__img_wrapper">
                    <img src={radio.src} alt="" />
                  </div>
                </label>
                <input type='radio'
                 name={radio.name}
                 value={radio.value}
                 checked={self.props.value === radio.value ? 'checked' : false}
                 onChange={self._handleChange.bind(radio)}
                 id={radioID} />
              </div>
    })
    return (<div className='layout-options-container'>
              {radios}
            </div>)
  }
})

export default LayoutOptions
