'use strict';

var _     = require('lodash');
var React = require('react');

var ChartFactory = require('chart');

module.exports = React.createClass({
  propTypes : {
    data    : React.PropTypes.array.isRequired,
    type    : React.PropTypes.string.isRequired,

    options : React.PropTypes.object
  },

  render : function () {
    return (
      <div className={'chart ' + _.kebabCase(this.props.type)}></div>
    );
  },

  componentDidMount : function () {
    this._chart = ChartFactory(
      this.props.type,
      React.findDOMNode(this),
      this.props.data,
      this.props.options);
  },

  componentDidUpdate : function () {
    this._chart.update(this.props.data, this.props.options);
  }
});
