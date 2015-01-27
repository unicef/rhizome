'use strict';

function interpolateSeries(s) {

}

exports.tweenSeries = function () {

};

exports.tweenLabel = function () {

};

exports.enterArea = function () {
	var area = d3.svg.area();

	function factory(d) {
		var start = d.map(function (p) {
			return { y: 0, y0: p.y0 };
		});

		var interpolator = d3.interpolateArray(start, d);

		return function (t) {
			return area(interpolator(t));
		};
	}

	factory.area = function (value) {
		if (!arguments.length) {
			return area;
		}

		area = value;
		return factory;
	};

	return factory;
};
