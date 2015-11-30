import React from 'react'

export default React.createClass({
  propTypes: {
    values: React.PropTypes.array.isRequired,
    value: React.PropTypes.number.isRequired,
    name: React.PropTypes.string.isRequired,
    prefix: React.PropTypes.string,
    horizontal: React.PropTypes.bool,
    title: React.PropTypes.string,
    onChange: React.PropTypes.func.isRequired
  },
  getDefaultProps: function () {
    return {
      prefix: '',
      horizontal: false
    }
  },
  render: function () {
    var radios = this.props.values.map((radio, index) => {
      return (
        <div key={radio.value} className={this.props.horizontal ? 'horizontal' : null}>
          <input type='radio' name={this.props.name} id={`${this.props.prefix}${radio.value}`}
            value={radio.value}
            checked={this.props.value === index ? 'checked' : false}
            onChange={this.props.onChange.bind(null, index)}/>
          <label htmlFor={`${this.props.prefix}${radio.value}`}>{radio.title}</label>
        </div>
      )
    })
    return (
      <div className='radio-group-container'>
        <h4>{this.props.title}</h4>
        {radios}
      </div>
    )
  }
})
