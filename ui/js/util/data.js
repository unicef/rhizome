'use strict';

function defined(value) {
	return value !== null &&
		typeof value !== 'undefined' &&
		Math.abs(value) !== Infinity &&
		!isNaN(value);
}

function min(data, accessor) {
	var m = Infinity;

	accessor = accessor || Number;

	if (data instanceof Array) {
		for (var i = data.length - 1; i >= 0; i--) {
			m = Math.min(m, min(data[i], accessor));
		}
	} else {
		var v = accessor(data);

		if (defined(v)) {
			m = Math.min(m, v);
		}
	}

	return m;
}

function max(data, accessor) {
	var m = -Infinity;

	accessor = accessor || Number;

	if (data instanceof Array) {
		for (var i = data.length - 1; i >= 0; i--) {
			m = Math.max(m, max(data[i], accessor));
		}
	} else {
		var v = accessor(data);

		if (defined(v)) {
			m = Math.max(m, v);
		}
	}

	return m;
}

module.exports = {
	min    : min,
	max    : max,
	defined: defined
};
