import React from 'react'

class SwitchButton extends React.Component {

    static propTypes = {
      id: React.PropTypes.string,
      name: React.PropTypes.string,
      title: React.PropTypes.string,
      label: React.PropTypes.string,
      labelRight: React.PropTypes.string,
      defaultChecked: React.PropTypes.string,
      theme: React.PropTypes.string,
      checked: React.PropTypes.string,
      onChange: React.PropTypes.func
    }

    static defaultProps = {
      id: '',
      name: 'switch-button',
      title: '',
      label: '',
      labelRight: '',
      defaultChecked: '',
      theme: 'switch-button-flat-round',
      checked: null,
      onChange: this.handleChange
    }

    handleChange() {
      // Override
    }

    render() {
      const id = this.props.id || this.props.name
      let label
      let labelRight

      if (this.props.label != '') {
        label = <label htmlFor={id}>{this.props.label}</label>
      }

      if (this.props.labelRight != '') {
        labelRight = <label htmlFor={id}>{this.props.labelRight}</label>
      }

      return (
        <div className={'switch-button ' + this.props.theme} >
          {label}
          <input
            id={id}
            value={1}
            type='checkbox'
            name={this.props.name}
            checked={this.props.checked}
            onChange={this.props.onChange}
            defaultChecked={this.props.defaultChecked}
          />
          <label htmlFor={id}></label>
          {labelRight}
        </div>
      )
    }

  }

export default SwitchButton