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

  shouldComponentUpdate : function (nextProps, nextState) {
    return nextState.opening || !_.isEqual(this.props, nextProps);
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

      if (!this.layer) {
        var menu = this.menu = (
          <Menu x={x} y={offset.bottom} {...props}>
            {items}
          </Menu>
        );

        this.layer = new Layer(document.body, function () {
          return menu;
        });

        this.layer.render();
        window.addEventListener('keyup', this);
      }
    } else if (this.layer) {
      this.layer.destroy();
      this.layer = null;
      this.menu = null;
      window.removeEventListener('keyup', this);
    }
  },

  _toggleMenu : function () {
    var open = !this.state.open;
    var opening = open;
    this.setState({
      open    : open,
      opening : opening
    });
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
