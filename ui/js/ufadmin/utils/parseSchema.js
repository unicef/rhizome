var _ = require('lodash');

module.exports = function parseSchema(response) {
	// parse our old json-table-esque schema into a legit JSON schema
	// http://json-schema.org/

	console.log('LOGGING PARSE CSCHEMA')
	console.log(response.objects)
	//return response.objects;
	var fields = ['id']
	var schema = {
		$schema: "http://json-schema.org/draft-04/schema#",
		title: "table_schema",
		type: "array",
		items: {
			title: "table_row",
			type: "object",
			properties: _(fields).map(field => {
				return [field.name, _.transform(field, (result, val, key) => {
					// if(key === 'type' && val === 'datetime') {
					// 	result.type = 'string';
					// 	result.format = 'date-time';
					// } else if(key === 'constraints') {
					// 	if(val && val.items && val.items.oneOf && val.items.oneOf.length) {
					// 		result.items = {type: typeof val, enum: val.items.oneOf};
					// 	}
					// } else if(_.includes(['type', 'title'], key)) {
					result[key] = val;
					// }
				})]
			}).object().value()
		}
	};
	console.log(schema.items)
	console.log('schema DATA above')
	return schema;
};
