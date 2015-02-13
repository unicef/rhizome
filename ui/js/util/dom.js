/* global window, MouseEvent */
'use strict';

var _ = require('lodash');

function intStyle(el, property) {
	var style = window.getComputedStyle(el);

	return parseInt(style.getPropertyValue(property), 10);
}

function dimensions(el, includeMargins) {
	var dims = {
		height: el.offsetHeight,
		width: el.offsetWidth
	};

	if (includeMargins) {
		dims.height += intStyle(el, 'margin-top') + intStyle(el, 'margin-bottom');
		dims.width += intStyle(el, 'margin-left') + intStyle(el, 'margin-right');
	}

	return dims;
}

function offset(el) {
	var off = {
		top   : el.offsetTop,
		right : 0,
		bottom: 0,
		left  : el.offsetLeft
	};

	var dims      = dimensions(el, true);
	var parent    = el.offsetParent || document.body;

	if (parent) {
		off.bottom = parent.scrollHeight - (off.top + dims.height);
		off.right  = parent.scrollWidth - (off.left + dims.width);
	}

	return off;
}

function documentOffset(el) {
	var bbox = el.getBoundingClientRect();
	var doc  = el.ownerDocument.documentElement;

	return {
		top   : bbox.top + doc.clientTop + window.pageYOffset,
		right : bbox.right + doc.clientLeft + window.pageXOffset,
		bottom: bbox.bottom + doc.clientTop + window.pageYOffset,
		left  : bbox.left + doc.clientLeft + window.pageXOffset,
	};
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

function contentArea(el) {
	return {
		width: el.clientWidth - intStyle(el, 'padding-left') - intStyle(el, 'padding-right'),
		height: el.clientHeight - intStyle(el, 'padding-top') - intStyle(el, 'padding-bottom')
	};
}


module.exports = {
	documentOffset: documentOffset,
	viewportOffset: viewportOffset,
	contains      : contains,
	dimensions    : dimensions,
	contentArea   : contentArea
};
