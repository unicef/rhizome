'use strict';

var _         = require('lodash');
var d3        = require('d3');
var moment    = require('moment');
var React     = require('react');

var colors    = require('colors');
var data      = require('util/data');
var hoverLine = require('./behavior/hover-line');
var label     = require('./renderer/label');


function _draw(el, props, state) {
  var svg    = d3.select(el);
  var series = props.series || [];
  var width  = Math.max(state.width - props.margin.left - props.margin.right, 0);
  var height = Math.max(state.height - props.margin.top - props.margin.bottom, 0);

  var x = _.flow(props.x.get, props.x.scale.range([0, width]));
  var y = _.flow(props.y.get, props.y.scale.range([height, 0]));

  var range  = props.y.scale.domain();

  // Set up the hover interaction
  // svg.select('svg')
  //  .call(hoverLine()
  //    .width(state.contentWidth)
  //    .height(state.contentHeight)
  //    .top(-props.margin.top)
  //    .xFormat(x.tickFormat)
  //    .yFormat(y.tickFormat)
  //    .x(props.x.get)
  //    .y(props.y.get)
  //    .xScale(xScale)
  //    .yScale(yScale)
  //    .diff(props.diffX)
  //    .seriesName(props.getSeriesName)
  //    .sort(true)
  //    .datapoints(_(series).map(props.getValues).flatten().value())
  //  );

  var g = svg.select('.data')
    .selectAll('.series')
    .data(series, props.getSeriesName);

  g.enter()
    .append('g')
    .attr('class', 'series');

  g.style({
    'fill'   : props.getColor,
    'stroke' : props.getColor
  });

  g.exit().remove();

  var path = g.selectAll('path')
    .data(function (d) { return [props.getValues(d)]; });

  path.enter().append('path');

  path.transition()
    .duration(500)
    .attr('d', d3.svg.line().x(x).y(y))

  var point = g.selectAll('circle')
    .data(props.getValues);

  point.enter()
    .append('circle')
    .attr({
      'cx' : x,
      'cy' : y,
      'r'  : 0
    });

  point.transition()
    .duration(500)
    .attr({
      'cx' : x,
      'cy' : y,
      'r'  : 3
    });

  point.exit()
    .transition()
    .duration(500)
    .attr('r', 0)
    .remove();

  var labels = _(series)
    .map(function (d) {
      var last = _.max(props.getValues(d), props.x.get);
      var v    = props.y.get(last);

      return {
        text    : props.getSeriesName(d) + ' ' + _.get(props.y, 'format', String)(v),
        x       : x(last),
        y       : y(last),
        defined : _.isFinite(v)
      };
    })
    .filter('defined')
    .sortBy('y')
    .value();

  svg.select('.annotation')
    .selectAll('.series.label')
    .data(labels)
    .call(label()
      .addClass('series')
      .width(width)
      .height(height)
      .align(false));

  var gx = svg.select('.x.axis')
    .call(d3.svg.axis()
      .tickFormat(_.get(props.x, 'format', String))
      .outerTickSize(0)
      .ticks(_.get(props.x, 'ticks', 3))
      .scale(props.x.scale)
      .orient('bottom'));

  // Prevent labels from overflowing the left and right edges of the SVG
  var svgBox = el.getBoundingClientRect();
  gx.selectAll('text')
   .attr('dx', function () {
     var bbox = this.getBoundingClientRect();
     var dx = null;

     if (bbox.right > svgBox.right) {
       dx = svgBox.right - bbox.right;
     }

     if (bbox.left < svgBox.left) {
       dx = svgBox.left - bbox.left;
     }

     return dx;
   });

  var gy = svg.select('.y.axis')
    .call(d3.svg.axis()
      .tickFormat(_.get(props.y, 'format', String))
      .tickSize(width)
      .ticks(_.get(props.y, 'ticks', 3))
      .scale(props.y.scale)
      .orient('right'));

  gy.selectAll('text')
    .attr({
      'x' : 4,
      'dy': -4
    });

  gy.selectAll('g').classed('minor', function (d) {
    return d !== range[0];
  });
}

module.exports = React.createClass({
	getDefaultProps : function () {
		return {
			series : [],
      x : {
        scale  : d3.time.scale(),
        get    : _.property('x'),
        format : d3.format('')
      },
      y : {
        scale  : d3.scale.linear(),
        get    : _.property('y'),
        format : d3.format(',.0f'),
        ticks  : 5
      },
      margin : {
        top    : 24,
        right  : 0,
        bottom : 24,
        left   : 0
      },
      getColor      : _.property('color'),
      getSeriesName : _.property('name'),
      getValues     : _.property('values'),
      aspect        : 1.618
		};
	},

  getInitialState : function () {
    return {
      height : 0,
      width  : 0,
      labels : []
    }
  },

  shouldComponentUpdate : function (nextProps, nextState) {
    // Update if any of the dimensions have changed.
    var shouldUpdate = !(nextState.width === this.state.width &&
      nextState.height === this.state.height &&
      _.isEqual(nextProps.margin, this.props.margin));

    if (!shouldUpdate) {
      _draw(React.findDOMNode(this), nextProps, nextState);
    }

    return shouldUpdate;
  },

  render : function () {
    var width         = Math.max(this.state.width, 0);
    var height        = Math.max(this.state.height, 0);
    var left          = Math.max(this.props.margin.left, 0);
    var top           = Math.max(this.props.margin.top, 0);
    var contentHeight = Math.max(height - top - this.props.margin.bottom, 0);
    var contentWidth  = Math.max(width - left - this.props.margin.right, 0);

    return (
      <svg className='line' viewBox={'0 0 ' + width + ' ' + height}>
        <rect className='bg'
          x={left}
          width={contentWidth}
          height={contentHeight + top}></rect>

        <g transform={'translate(' + left + ',' + top + ')'}>
          <g className='y axis'></g>
          <g className='x axis'
            transform={'translate(0,' + contentHeight + ')'}></g>
          <g className='data'></g>
          <g className='annotation'></g>
        </g>
      </svg>
    )
  },

  componentDidMount : function () {
    window.addEventListener('resize', this._resize);
    this._resize();
  },

  _resize : function () {
    var el    = React.findDOMNode(this);
    var width = el.parentNode.clientWidth;

    this.setState({
      width  : width,
      height : width / this.props.aspect
    });
  },

  componentDidUpdate : function () {
    _draw(React.findDOMNode(this), this.props, this.state);
  },

  componentWillUnmount : function () {
    window.removeEventListener('resize', this._resize);
  }
});
