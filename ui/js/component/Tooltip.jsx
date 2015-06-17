'use strict';

var _ = require('lodash');
var React = require('react');

// Imports

var Tooltip = React.createClass({
  propTypes : {
    top  : React.PropTypes.number.isRequired,
    left : React.PropTypes.number.isRequired
  },

  render : function () {
    return (
      <div className='tooltip' style={this.props}>
        {this.props.children}
      </div>
    );
  },
});

module.exports = Tooltip;
