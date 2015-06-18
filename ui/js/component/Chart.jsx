'use strict';

var _     = require('lodash');
var React = require('react');

var ChartFactory = require('chart');

module.exports = React.createClass({
  propTypes : {
    data    : React.PropTypes.array.isRequired,
    type    : React.PropTypes.string.isRequired,

    id      : React.PropTypes.string,
    options : React.PropTypes.object,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var overlay;

    if (this.props.loading || _.isEmpty(this.props.data)) {
      var position = _.get(this.props, 'options.margin', {
        top    : 0,
        right  : 0,
        bottom : 0,
        left   : 0
      });

      var message = (this.props.loading) ?
        (<span><i className='fa fa-spinner fa-spin'></i>&nbsp;Loading</span>) :
        (<span className='empty'>No data</span>);

      overlay = (
        <div style={position} className='overlay'>
          <div>
            <div>{message}</div>
          </div>
        </div>
      );
    }

    return (
      <div id={this.props.id} className={'chart ' + _.kebabCase(this.props.type)}>
        {overlay}
      </div>
    );
  },

  componentDidMount : function () {
    this._chart = ChartFactory(
      this.props.type,
      React.findDOMNode(this),
      this.props.data,
      this.props.options);
  },

  componentWillReceiveProps: function(nextProps) {
  	if(nextProps.type != this.props.type)
  	{
  	    React.findDOMNode(this).innerHTML = '';
  		this._chart = ChartFactory(
  		    nextProps.type,
  		    React.findDOMNode(this),
  		    this.props.data,
  		    this.props.options);
  	}
  },

  componentDidUpdate : function () {
    this._chart.update(this.props.data, this.props.options);
  }
});
