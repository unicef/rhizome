import React, {Component, PropTypes} from 'react'

import IconButton from 'components/button/IconButton'
import Dropdown from 'components/dropdown/Dropdown'

class Select extends Dropdown {

  static propTypes = {
    items: PropTypes.array,
    className: PropTypes.string,
    text: PropTypes.string.isRequired,
    icon: PropTypes.string,
    searchable: PropTypes.bool,
    onSearch: PropTypes.func
  }

  static defaultProps = {
    icon: 'fa-bars',
    onSearch: () => null
  }

  componentWillReceiveProps = (nextProps) => {
    if (nextProps.text !== this.props.text) {
      this.setState({ open: false })
    }
  }

  render = () => {
    return (
      <div className={'dropdown-list ' + this.props.className} onClick={this._toggleMenu}>
        <div className='dropdown-list-text'>{this.props.text}</div>
        {
          this.props.icon ? (
            <IconButton onClick={this._toggleMenu} icon={this.props.icon} className='right'/>
          ) : null
        }
      </div>
    )
  }
}

export default Select
