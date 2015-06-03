'use strict';

var _     = require('lodash');
var React = require('react');
var Layer = require('react-layer');

var Menu = require('component/Menu.jsx');

var dom = require('util/dom');

var ButtonMenu = React.createClass({
  propTypes : {
    text : React.PropTypes.string,

    icon : React.PropTypes.string,
    size : React.PropTypes.string
  },

  getDefaultProps : function () {
    return {
      icon : 'fa-bars',
    }
  },

  getInitialState : function () {
    return {
      open : false
    };
  },

  render : function () {
    var icon = this.props.icon ?
      (<i className={['fa', this.props.icon, this.props.size].join(' ')} />) :
      null;

    var classes = 'menu-button';

    if (this.state.open) {
      classes += ' open';
    }

    return (
      <span className={classes}>
        <a className="button" role="button" onClick={this._toggleMenu}>
          {icon} {this.props.text}
        </a>
      </span>
    );
  },

  componentDidUpdate : function () {
    if (this.state.open) {
      var items  = this.props.children;
      var offset = dom.documentOffset(React.findDOMNode(this));
      var props  = _.omit(this.props, 'text', 'icon', 'size');

      if (!this.layer) {
        this.layer = new Layer(document.body, function () {
          return (
            <Menu x={offset.left} y={offset.bottom} {...props}>
              {items}
            </Menu>
          );
        });
      }

      this.layer.render();
    } else if (this.layer) {
      this.layer.destroy();
      this.layer = null;
    }
  },

  _toggleMenu : function () {
    console.log(this.state.open ? 'close!' : 'open!');
    this.setState({ open : !this.state.open });
  }
});

module.exports = ButtonMenu;
