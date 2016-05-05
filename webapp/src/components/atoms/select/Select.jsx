import React, {Component, PropTypes} from 'react'

import IconButton from 'components/atoms/button/IconButton'
import Dropdown from 'components/atoms/dropdown/Dropdown'

class Select extends Dropdown {

  static propTypes = {
    className: React.PropTypes.string,
    text: React.PropTypes.string.isRequired,
    icon: React.PropTypes.string,
    searchable: React.PropTypes.bool,
    onSearch: React.PropTypes.func
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
          {
            this.props.icon ? (
              <div className='dropdown-list-text'>
                {this.props.text}
                <IconButton onClick={this._toggleMenu} icon={this.props.icon} className='right'/>
              </div>
            ) : (
              <div>
                <div className='dashboard-nav__text'>{this.props.text}</div>
              </div>
            )
          }
      </div>
    )
  }
}

export default Select
