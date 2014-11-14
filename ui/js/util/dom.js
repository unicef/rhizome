/* global window, MouseEvent */
'use strict';

var _ = require('lodash');

function documentOffset(el) {
	if (!el.offsetParent) {
		return {
			top: el.offsetTop,
			left: el.offsetLeft
		};
	}

	return _.reduce(documentOffset(el.offsetParent), function (result, offset, key) {
		result[key] += offset;
		return result;
	}, { top: el.offsetTop, left: el.offsetLeft });
}

function viewportOffset(el) {
	return _.reduce({ top: window.pageYOffset, left: window.pageXOffset }, function (result, offset, key) {
		result[key] -= offset;
		return result;
	}, documentOffset(el));
}

function contains(el, pt) {
	var offset = documentOffset(el);

	if (pt instanceof MouseEvent) {
		pt = {
			x: pt.pageX,
			y: pt.pageY
		};
	}

	var x = pt.x - offset.left,
		y = pt.y - offset.top;

	return x >= 0 && x <= el.offsetWidth &&
		y >= 0 && y <= el.offsetHeight;
}

function dimensions(el, includeMargins) {
	var dims = {
		height: el.offsetHeight,
		width: el.offsetWidth
	};

	if (includeMargins) {
		var style = window.getComputedStyle(el);

		dims.height += parseInt(style.getPropertyValue('margin-top'), 10) +
				parseInt(style.getPropertyValue('margin-bottom'), 10);

		dims.width += parseInt(style.getPropertyValue('margin-left'), 10) +
				parseInt(style.getPropertyValue('margin-right'), 10);
	}

	return dims;
}

module.exports = {
	documentOffset: documentOffset,
	viewportOffset: viewportOffset,
	contains: contains,
	dimensions: dimensions
};
