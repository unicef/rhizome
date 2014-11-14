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

module.exports = {
	documentOffset: documentOffset,
	viewportOffset: viewportOffset,
	contains: contains
};
