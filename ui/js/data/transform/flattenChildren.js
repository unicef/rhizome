var _ = require('lodash');

/**
 * Assemble a flat array with all and object's nested children (deep)
 */
function flattenChildren(root, childrenKey, arr) {
	'use strict';
	
	arr = arr || [];

	if (root[childrenKey] && _.isArray(root[childrenKey])) {
		_.forEach(root[childrenKey], function(child) {
			arr.push(child);
			flattenChildren(child, childrenKey, arr);
		});
	}

	return arr;
}

module.exports = flattenChildren;