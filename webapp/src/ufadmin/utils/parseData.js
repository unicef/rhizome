var _ = require('lodash')

module.exports = function parseData (response) {
  var my_data = {
    items: {
      properties: _(response.objects).map(object => {
        return [object.id, _.transform(field, (result, val, key) => {
          result[key] = val
        })]
      }).object().value()
    }
  }
  return my_data.items
}
