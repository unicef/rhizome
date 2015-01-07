'use strict';

function defined(value) {
	return value !== null &&
		typeof value !== 'undefined' &&
		Math.abs(value) !== Infinity &&
		!isNaN(value);
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

function parseBool(value) {
	if (value instanceof String) {
		return value === 'true';
	}

	return Boolean(value);
}

function rename(obj, mapping) {
	var o = {};

	for (var k in obj) {
		o[mapping[k] || k] = obj[k];
	}

	return o;
}

module.exports = {
	defined  : defined,
	max      : max,
	min      : min,
	parseBool: parseBool,
	rename   : rename
};
