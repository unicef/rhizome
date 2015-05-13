'use strict';

var _     = require('lodash');
var d3    = require('d3');
var React = require('react');

var dom     = require('util/dom');
var palette = require('util/colorbrewer');
var util    = require('util/data');

module.exports = React.createClass({
	getDefaultProps : function () {
		return {
      cellSize      : 16,
			getId         : function (d, i) { return d.id || i;},
			getHeaderText : _.identity,
			getSeriesName : function (s) { return s.name; },
      getSortValue  : function (s, sortCol) {
        var val = sortCol == null ?
          props.getSeriesName(s) :
          props.getValue(props.getValues(s)[sortCol]);

        return val;
      },
			getValue      : function (d) { return d.value; },
			getValues     : function (s) { return s.values; },
			headers       : [],
			margin        : {
				left   : 120,
				top    : 120,
				right  : 0,
				bottom : 0
			},
			onClick       : null,
      onColHover    : _.noop,
			onMouseOut    : null,
			onMouseOver   : null,
			scale         : d3.scale.quantile().domain([0, 1]).range(palette.YlOrRd[9]),
			series        : [],
			sortable      : true
		};
	},

	getInitialState : function () {
		return {
			height  : 1024,
			sortCol : null,
			width   : 1024
		};
	},

	componentWillReceiveProps : function (nextProps) {
		var size = nextProps.cellSize;

		var h = nextProps.series.length * size +
			nextProps.margin.top +
			nextProps.margin.bottom;

		var w = _(nextProps.series).map(nextProps.getValues).max(_.size).length * size +
			nextProps.margin.left +
			nextProps.margin.right;

		this.setState({
			height : h,
			width  : w
		});
	},

	shouldComponentUpdate : function (nextProps, nextState) {
		var update = !_.isEqual(nextProps.margin, this.props.margin) ||
			this.state.width != nextState.width ||
			this.state.height != nextState.height;

		if (!update) {
			this._draw(nextProps, nextState);
		}

		return update;
	},

	render : function () {
		var className = 'heatmap';

		if (this.props.sortable) {
			className += ' sortable';
		}

		return (
			<div className="chart">
				<svg className={className} ref="svg"
					width={this.state.width}
					height={this.state.height}>

					<g transform={'translate(' + this.props.margin.left + ',' + this.props.margin.top + ')'}>
						<g className="y axis"></g>
						<g className="x axis"></g>
						<g className="data" onMouseOut={this._onRowOut}></g>
					</g>
				</svg>
			</div>
		);
	},

  componentDidUpdate : function () {
    this._draw(this.props, this.state);
  },

	_draw : function (props, state) {
		var self    = this;

		// Calculate the dimensions for the heatmap based on the width of its
		// containing element
		// var contentArea = dom.contentArea(React.findDOMNode(this).parentElement);
		var width  = state.width - props.margin.left - props.margin.right;
		var height = state.height - props.margin.top - props.margin.bottom;

		var fill = function (d) {
			var v = props.getValue(d);

			return v != null ? props.scale(v) : 'transparent';
		};

		var xScale = d3.scale.ordinal()
			.domain(_.map(props.headers, props.getHeaderText))
			.rangeBands([0, width], .1);

		var x = function (d, i) {
			var xpos = xScale(props.getHeaderText(props.headers[i]));
			return xpos;
		};

    var sortValue = _.partial(props.getSortValue, _, state.sortCol);

		var yScale = d3.scale.ordinal()
			.domain(_(props.series).sortBy(sortValue).map(props.getSeriesName).value())
			.rangeBands([0, height], .1);

		var y = _.flow(props.getSeriesName, yScale);

		var transform = function (d, i) {
			return 'translate(0,' + y(d) + ')';
		};

		var series = props.series;

		var svg = d3.select(React.findDOMNode(this.refs.svg));
		var row = svg.select('.data').selectAll('.row').data(series, props.getId);

		row.enter().append('g')
			.attr({
				'class'     : 'row',
				'transform' : transform,
			});

		row.exit()
			.transition().duration(300)
			.style('opacity', 0)
			.remove();

		row.on('mouseover', this._onRowHover)
			.transition().duration(750)
			.attr('transform', transform);

		// Add cells to each row
		var cell = row.selectAll('.cell').data(props.getValues, props.getId);

		cell.transition()
			.duration(500)
			.style('fill', fill)
			.attr({
				'height' : yScale.rangeBand(),
				'width'  : xScale.rangeBand(),
				'x'      : x
			});

		cell.enter().append('rect')
			.attr({
				'class'  : 'cell',
				'height' : yScale.rangeBand(),
				'x'      : x,
				'width'  : xScale.rangeBand(),
			})
			.style({
				'opacity' : 0,
				'fill'    : fill
			})
			.transition().duration(500)
			.style('opacity', 1);

		cell.exit()
			.transition().duration(300)
			.style('opacity', 0)
			.remove();

		cell
			.style('cursor', _.isFunction(props.onClick) ? 'pointer' : 'initial')
			.on('mouseover', props.onMouseOver)
			.on('mouseout', props.onMouseOut)
			.on('click', props.onClick);

		svg.select('.x.axis')
			.transition().duration(300)
			.call(d3.svg.axis()
				.scale(xScale)
				.orient('top')
				.outerTickSize(0));

		svg.selectAll('.x.axis text')
				.style({
          'text-anchor' : 'start',
          'font-weight' : function (d, i) {
            return (i === state.sortCol) ?
              'bold' :
              'normal';
            }
        })
				.attr('transform', 'translate(' + (xScale.rangeBand() / 2) + ',0) rotate(-45)')
        .on('click', props.sortable ? this._setSort : null)
        .on('mouseover', this._onHeaderMouseOver)
        .on('mouseout', this._onHeaderMouseOut);

		svg.select('.y.axis')
			.transition().duration(300)
			.call(d3.svg.axis()
				.scale(yScale)
				.orient('left')
				.outerTickSize(0));
	},

  _onHeaderMouseOver : function (d, i) {
    this.props.onColHover(d, i, true);
  },

  _onHeaderMouseOut : function (d, i) {
    this.props.onColHover(d, i, false);
  },

	_onRowHover : function (d, row) {
		d3.select(React.findDOMNode(this.refs.svg)).selectAll('.row')
			.transition().duration(300)
			.style('opacity', function (d, i) {
				return i === row ? 1 : 0.4;
			});
	},

	_onRowOut : function () {
		d3.select(React.findDOMNode(this.refs.svg)).selectAll('.row')
			.transition().duration(300)
			.style('opacity', 1);
	},

	_setSort : function (d, i) {
		this.setState({sortCol : (i === this.state.sortCol) ? null : i});
	}

});
