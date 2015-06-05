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
    size : React.PropTypes.string,

    multi : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      icon  : 'fa-bars',
      multi : false
    }
  },

  getInitialState : function () {
    return {
      open : false
    };
  },

  componentWillReceiveProps : function (nextProps) {
    if (!this.multi && nextProps.text !== this.props.text) {
      this.setState({ open : false });
    }
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

      var x = (offset.right + offset.left) / 2

      this.menu = (
        <Menu x={x} y={offset.bottom} {...props}>
          {items}
        </Menu>
      );

      if (!this.layer) {
        var self = this;
        this.layer = new Layer(document.body, function () {
          return self.menu;
        });
        window.addEventListener('keyup', this);
      }

      this.layer.render();
    } else if (this.layer) {
      this.layer.destroy();
      this.layer = null;
      this.menu = null;

      // Clear out the search patterns that the parent component is necessarily
      // using to provide filtered menu items.
      this.props.onSearch('');
      window.removeEventListener('keyup', this);
    }
  },

  _toggleMenu : function () {
    this.setState({open : !this.state.open });
  },

  handleEvent : function (evt) {
    var handler = 'on' + _.capitalize(evt.type);
    _.get(this, handler, _.noop)(evt);
  },

  onKeyup : function (evt) {
    if (evt.keyCode === 27) {
      // On escape pressed, close the menu
      this.setState({ open : false });
    }
  }
});

module.exports = ButtonMenu;
