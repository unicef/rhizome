import React, {Component, PropTypes} from 'react'

class DropdownMenuItem extends Component {

  static propTypes = {
    key: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
    classes: PropTypes.string
  }

  render = () => {
    return (
      <li key={this.props.key} className={this.props.classes}>
        <a role='menuitem' onClick={this.props.onClick}>
          {this.props.text}
        </a>
      </li>
    )
  }
}

export default DropdownMenuItem
