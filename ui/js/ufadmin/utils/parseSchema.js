var _ = require('lodash');

module.exports = function parseSchema(data) {

	console.log('response')
	console.log(data)


	if (data.page_definition){
		var prepped_data = page_definition
	}
	else {
		var prepped_data = data.objects
	}

	console.log(prepped_data)

	var schema = {
		$schema: "http://json-schema.org/draft-04/schema#",
		title: "table_schema",
		type: "array",
		items: {
			title: "table_row",
			type: "object",
			properties: _(prepped_data.fields).map(field => {
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
	return schema;
};
