module.exports = function sort(accessor) {
	'use strict';

	function transform(data) {
		data.objects.sort(function (a, b) {
			return accessor(a) < accessor(b) ? -1 : 1;
		});

		return data;
	}

	return transform;
};
