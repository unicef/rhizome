'use strict';

var _ = require('lodash');
var React = require('react');

var TitleMenu = React.createClass({
  mixins : [
    require('mixin/MenuControl')
  ],

  propTypes : {
    text       : React.PropTypes.string.isRequired,

    icon       : React.PropTypes.string,
    searchable : React.PropTypes.bool,
    onSearch   : React.PropTypes.func
  },

  getDefaultProps : function () {
    return {
      icon : 'fa-bars',
    };
  },

  componentWillReceiveProps : function (nextProps) {
    if (nextProps.text !== this.props.text) {
      this.setState({ open : false });
    }
  },

  render : function () {
    return (
      <span>
        {this.props.text}&nbsp;
        <a className='menu-button fa-stack' onClick={this._toggleMenu}>
          <i className='fa fa-stack-2x fa-circle'></i>
          <i className={'fa fa-stack-1x ' + this.props.icon}></i>
        </a>
      </span>
    );
  },

});

module.exports = TitleMenu;
