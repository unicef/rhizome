import React, {Component, PropTypes} from 'react'

class AsyncButton extends Component {

  constructor (props) {
    super(props)
  }

  static propTypes = {
    text: PropTypes.string,
    alt_text: PropTypes.string,
    isBusy: PropTypes.bool,
    onClick: PropTypes.func.isRequired,
    icon: PropTypes.string, // Fontawesome icons. Leave off the 'fa-'
    classes: PropTypes.string,
    style: PropTypes.string
  }

  static defaultProps = {
    text: null,
    icon: null,
    classes: ' button '
  }

  render () {
    const icon_string = this.props.isBusy ? 'spinner fa-spin saving-icon' : this.props.icon
    return (
      <button className={this.props.classes} onClick={this.props.onClick} style={this.props.style}>
        { this.props.icon ? <i className={'fa fa-' + icon_string}></i> : '' }
        <span>
          { this.props.isBusy ? this.props.alt_text : this.props.text }
        </span>
      </button>
    )
  }
}

export default AsyncButton
