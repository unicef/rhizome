import React from 'react'

export default class CheckBoxGroup extends React.Component {
  constructor (props) {
    super(props)
  }
  static defaultProps = {
    prefix: ''
  }
  static propTypes = {
    values: React.PropTypes.array.isRequired,
    value: React.PropTypes.number.isRequired,
    name: React.PropTypes.string.isRequired,
    prefix: React.PropTypes.string,
    title: React.PropTypes.string,
    onChange: React.PropTypes.func.isRequired
  }
  render () {
    let checkboxes = this.props.values.map((check, index) => {
      return (
        <div key={check.value}>
          <input type='checkbox' name={this.props.name} id={`${this.props.prefix}${check.value}`}
            value={check.value}
            checked={this.props.value.indexOf(index) >= 0 ? 'checked' : false}
            onChange={this.props.onChange.bind(null, index)} />
          <label htmlFor={`${this.props.prefix}${check.value}`}>{check.title}</label>
        </div>
      )
    })
    return (
      <div className='checkbox-group'>
        <h4>{this.props.title}</h4>
        {checkboxes}
      </div>
    )
  }
}
