import React, {Component, PropTypes} from 'react'

class AsyncButton extends Component {

  constructor (props) {
    super(props)
  }

  static propTypes = {
    text: PropTypes.string,
    alt_text: PropTypes.string,
    disabled: PropTypes.bool,
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
    const props = this.props
    const icon_string = props.isBusy ? 'spinner fa-spin saving-icon' : props.icon
    return (
      <button disabled={props.disabled} className={props.classes} onClick={props.onClick} style={props.style}>
        { props.icon ? <i className={'fa fa-' + icon_string}></i> : '' }
        <span>
          { props.isBusy ? props.alt_text : props.text }
        </span>
      </button>
    )
  }
}

export default AsyncButton
