'use strict';

var _ = require('lodash');
var React = require('react');

var NavMenuItem = React.createClass({
  propTypes : {
    href : React.PropTypes.string.isRequired
  },

  statics : {
    fromArray : function (arr) {
      return _.map(arr, function (item) {
        return (
          <NavMenuItem key={item.key} href={item.url}>{item.name}</NavMenuItem>
        );
      })
    }
  },

  render : function () {
    return (
      <li>
        <a role='menuitem' href={this.props.href}>
          {this.props.children}
        </a>
      </li>
    );
  },
});

module.exports = NavMenuItem;
