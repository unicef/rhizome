'use strict'

var _ = require('lodash')
var React = require('react')

var NavMenuItem = React.createClass({
  propTypes: {
    href: React.PropTypes.string.isRequired,
    // children: React.PropTypes.string.array
  },

  statics: {
    fromArray: function (arr) {
      return _.map(arr, function (item) {
        return (
          <NavMenuItem key={item.key} href={item.href}>{item.title}</NavMenuItem>
        )
      })
    }
  },

  render: function () {
    return (
      <li>
        <a role='menuitem' href={this.props.href} tabIndex='-1'>
          {this.props.children}
        </a>
      </li>
    )
  }
})

module.exports = NavMenuItem
