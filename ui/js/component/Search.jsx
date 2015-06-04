'use strict';

var React = require('react');

var Search = React.createClass({
  propTypes : {
    onChange : React.PropTypes.func.isRequired
  },

  getInitialState : function () {
    return {
      pattern : ''
    };
  },

  render : function () {
    var clear = this.state.pattern.length > 0 ?
      (
        <a className='clear-btn' onClick={this._clear}>
          <i className='fa fa-times-circle'></i>
        </a>
      ) :
      null;

    return (
      <div style={{ position : 'relative' }} role='search'>
        <input type="text" tabIndex="1" onChange={this._setPattern} value={this.state.pattern} />
        {clear}
      </div>
    );
  },

  _setPattern : function (e) {
    if (e.target.value.length > 2) {
      this.props.onChange(e.target.value);
    }

    this.setState({ pattern : e.target.value });
  },

  _clear : function () {
    if (this.state.pattern.length > 2) {
      this.props.onChange('');
    }

    this.setState({ pattern : '' });
  }
});

module.exports = Search;
