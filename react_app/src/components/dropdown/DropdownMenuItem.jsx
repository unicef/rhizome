import React, {Component, PropTypes} from 'react'


const DropdownMenuItem = (props) => (
  <li className={props.classes}>
    <a role='menuitem' onClick={props.onClick}>{props.text}</a>
  </li>
)

DropdownMenuItem.propTypes = {
  text: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  classes: PropTypes.string
}


export default DropdownMenuItem
