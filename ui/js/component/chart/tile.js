'use strict';

function tile() {
	var domain = [0, 1];
	var getValue = Object;

	function transform(data) {
		var tiles  = [];

		var previous = {
			lower: domain[0],
			value: getValue(data[0])
		};

		for (var i = 1, l = data.length; i < l; i++) {
			var v    = getValue(data[i]);
			var next = previous.value + (Math.abs(v - previous.value) / 2);

			previous.distance = next - previous.lower;
			tiles.push(previous);

			// Moving on to the next previous object
			previous = {
				lower: next,
				value: v
			};
		}

		previous.distance = domain[1] - previous.lower;
		tiles.push(previous);

		return tiles;
	}

	transform.domain = function (x) {
		if (!arguments.length) {
			return domain;
		}

		domain = x;
		return transform;
	};

	transform.value = function (x) {
		if (!arguments.length) {
			return getValue;
		}

		getValue = x;
		return transform;
	};

	return transform;
}

module.exports = tile;
