import _ from 'lodash'

export default function parseSchema (data) {
  var _data = _.isArray(data) ? data : Object.keys(data.objects[0])

  var fields = _data.map(f => {
    return {'name': f, 'title': f}
  })

  var schema = {
    $schema: 'http://json-schema.org/draft-04/schema#',
    title: 'table_schema',
    type: 'array',
    items: {
      title: 'table_row',
      type: 'object',
      properties: _(fields).map(field => {
        return [field.name, _.transform(field, (result, val, key) => {
          result[key] = val
        })]
      }).object().value()
    }
  }
  return schema
}
