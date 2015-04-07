'use strict';

var _  = require('lodash');

/**
 * @constructor
 */
function label() {
	var cls             = ['label'];
	var height          = 1;
	var text            = function (d) { return d.text; };
	var transitionSpeed = 300;
	var width           = 1;
	var x               = function (d) { return d.x; };
	var y               = function (d) { return d.y; };
	var align           = true;

	/**
	 * @private
	 * Find the center of a collection of bounding boxes.
	 */
	function findBounds(boxes) {
		var top    = Infinity;
		var right  = -Infinity;
		var bottom = -Infinity;
		var left   = Infinity;

		for (var i = boxes.length - 1; i >= 0; i--) {
			var b  = boxes[i];

			top    = Math.min(b.top, top);
			right  = Math.max(b.right, right);
			bottom = Math.max(b.bottom, bottom);
			left   = Math.min(b.left, left);
		}

		return {
			top   : top,
			right : right,
			bottom: bottom,
			left  : left,
			cx    : (right - left) / 2,
			cy    : (bottom - top) / 2,
		};
	}

	/**
	 * @private
	 * Reposition labels vertically so they don't overlap
	 *
	 * @param {Object} selection a D3 selection (probably of text elements)
	 *
	 * @author Manish Nag <nag@seedscientific.com
	 * @author Evan Sheehan <sheehan@seedscientific.com
	 */
	function splay(selection) {
		var l = selection.size();

		if (l < 2) {
			return;
		}

		var bboxes = new Array(l);
		var data   = new Array(l);

		// Retrive all of the bounding boxes for each element in the selection.
		// Because D3 selections can be multi-dimensional, we use the built-in
		// for-each loop instead of a map call to ensure that we get everything
		selection.each(function (d, i) {
			bboxes[i] = this.getBoundingClientRect();
			d._height = bboxes[i].height;
			data[i]   = d;
		});

		// We'll need these later to re-center the labels as close as possible to
		// their desired positions
		var origBounds = findBounds(bboxes);

		// Begin with the last label and shift any overlapping labels up
		var a, b, h;
		for (var i = l - 1; i > 0; i--) {
			a = data[i - 1];
			b = data[i];
			h = b._height;

			// Ensure that b is in bounds first
			b.y = Math.min(b.y, height);

			// Shift a up if it overlaps with b
			if (a.y > b.y - h) {
				a.y = b.y - h;
			}
		}

		// Now iterate over the labels from top to bottom, shifting labels down
		// as needed.
		for (i = 1; i < l; i++) {
			a = data[i - 1];
			b = data[i];
			h = b._height;

			// Ensure that a is in bounds first
			a.y = Math.max(a.y, 0);

			if (b.y - h < a.y) {
				b.y = a.y + h;
			}
		}

		// Recenter the labels
		var top    = data[0].y - data[0]._height;
		var bottom = data[data.length - 1].y;
		var center = (bottom - top) / 2;
		var delta  = center - origBounds.cy;

		// Apply the shift to all of the labels' data
		for (i = 0; i < l; i++) {
			data[i].y += delta;
		}
	}

	/**
	 * @private
	 * Return the text-anchor for a set of labels
	 *
	 * Calculates the text-anchor ("start" or "end") for a set of labels so that
	 * all labels are oriented the same way, and so that labels don't get clipped
	 * by the edge of the SVG. Prefer "start" over "end."
	 */
	function textAnchor(labels) {
		var anchor = 'start';

		labels.each(function (d) {
			var bbox = this.getBBox();

			if (d.x + bbox.width > width) {
				anchor = 'end';
			}
		});

		return anchor;
	}

	function calcAnchor(d, el) {
		var anchor = 'start';
		var bbox   = el.getBBox();

		if (d.x + bbox.width > width) {
			anchor = 'end';
		}

		return anchor;
	}

	function chart(labels) {
		labels.enter()
			.append('text')
			.style('opacity', 0)
			.attr({
				'dy': '-4',
				'x' : x,
				'y' : y
			})
			.text(text);

		labels
			.text(text)
			.attr('class', cls.join(' '))
			.transition()
			.duration(transitionSpeed)
			.attr({
				'x': x,
				'y': y,
			});

		// Fix overlaps
		splay(labels);

		// Redraw everything with new positions to fix overlaps
		var anchor = textAnchor(labels);
		var dx     = anchor === 'start' ? '4' : '-4';

		labels
			.transition()
			.duration(transitionSpeed)
			.attr({
				'x'          : x,
				'y'          : y,
				'dx'         : function (d) {
					if (align) {
						return dx;
					}

					return calcAnchor(d, this) === 'start' ? '4' : '-4';
				},
				'text-anchor': function (d) {
					if (align) {
						return anchor;
					}

					return calcAnchor(d, this);
				}
			})
			.style('opacity', 1);

			labels.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();
	}

	chart.addClass = function (value) {
		if (!chart.hasClass(value)) {
			cls.push(value);
		}

		return chart;
	};

	chart.align = function (value) {
		if (!arguments.length) {
			return align;
		}

		align = value;
		return chart;
	};

	chart.classes = function (value) {
		if (!arguments.length) {
			return cls;
		}

		if (_.isString(value)) {
			value = value.split(/\s+/);
		} else if (!_.isArray(value)) {
			value = [String(value)];
		}

		cls = value;

		return chart;
	};

	chart.hasClass = function (value) {
		return cls.indexOf(value) > -1;
	};

	chart.height = function (value) {
		if (!arguments.length) {
			return height;
		}

		height = value;
		return chart;
	};

	chart.removeClass = function (value) {
		var i = cls.indexOf(value);

		if (i > -1) {
			cls.splice(i, 1);
		}

		return chart;
	};

	chart.text = function (value) {
		if (!arguments.length) {
			return text;
		}

		text = value;
		return chart;
	};

	chart.transitionSpeed = function (value) {
		if (!arguments.length) {
			return transitionSpeed;
		}

		transitionSpeed = value;
		return chart;
	};

	chart.width = function (value) {
		if (!arguments.length) {
			return width;
		}

		width = value;
		return chart;
	};

	chart.x = function (value) {
		if (!arguments.length) {
			return x;
		}

		x = value;
		return chart;
	};

	chart.y = function (value) {
		if (!arguments.length) {
			return y;
		}

		y = value;
		return chart;
	};

	return chart;
}

module.exports = label;
