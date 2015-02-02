/* global document, window, MouseEvent */
'use strict';

var _ = require('lodash');

function intStyle(el, property) {
	var style = window.getComputedStyle(el);

	return parseInt(style.getPropertyValue(property), 10);
}

function offset(el) {
	var offset = {
		top : el.offsetTop,
		left: el.offsetLeft
	};

	var dims      = dimensions(el, true);
	var parent    = el.offsetParent || document.body;

	offset.bottom = parent.scrollHeight - (offset.top + dims.height);
	offset.right  = parent.scrollWidth - (offset.left + dims.width);

	return offset;
}

function documentOffset(el) {
	var off = offset(el);

	if (!el.offsetParent) {
		return off;
	}

	return _.reduce(documentOffset(el.offsetParent), function (result, off, key) {
		result[key] += off;
		return result;
	}, off);
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
		dims.height += intStyle(el, 'margin-top') + intStyle(el, 'margin-bottom');
		dims.width += intStyle(el, 'margin-left') + intStyle(el, 'margin-right');
	}

	return dims;
}

function contentArea(el) {
	return {
		width: el.clientWidth - intStyle(el, 'padding-left') - intStyle(el, 'padding-right'),
		height: el.clientHeight - intStyle(el, 'padding-top') - intStyle(el, 'padding-bottom')
	};
}


module.exports = {
	offset        : offset,
	documentOffset: documentOffset,
	viewportOffset: viewportOffset,
	contains      : contains,
	dimensions    : dimensions,
	contentArea   : contentArea
};
