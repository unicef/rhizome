'use strict';

/**
 * Map properties on an object to new properties.
 *
 * @param {Object} - mapping of property names to functions that calculate the
 *   value for the newly mapped property.
 *
 * Example:
 *     variables({ x: function (d) { return d.campaign.start_date; }})(data)
 *
 * Will create a property `x` on each objects in `data` whose value is
 * `campaign.start_date`.
 */
module.exports = function (mapping) {

	function transform(data) {
		for (var i = data.length - 1; i >= 0; i--) {
			var d = data[i];
			var keys = Object.keys(mapping);

			for (var j = keys.length - 1; j >= 0; j--) {
				var k = keys[j];

				// FIXME: There is a danger that a mapping could overwrite existing
				// properties.
				d[k] = mapping[k](d);
			}
		}

		return data;
	}

	return transform;
};
