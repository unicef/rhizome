'use strict';

var React = require('react');

var MenuControl = require('mixin/MenuControl');

var NavMenu = React.createClass({
  mixins : [
    require('mixin/MenuControl')
  ],

  propTypes : {
    text : React.PropTypes.string.isRequired,
    icon : React.PropTypes.string
  },

  render : function () {
    var display = !!this.props.icon ?
      (<span><i className={'fa fa-lg ' + this.props.icon}></i>&ensp;{this.props.text}</span>) :
      (<span>{this.props.text}</span>);

    return (
      <span>
        <a onClick={this._toggleMenu}>
          {display}&emsp;<i className='fa fa-chevron-down'></i>
        </a>
      </span>
    );
  }

});

module.exports = NavMenu;
