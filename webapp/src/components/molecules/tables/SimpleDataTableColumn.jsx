import React from 'react'
import InterfaceMixin from 'utilities/tech_debt/InterfaceMixin'

let SimpleDataTableColumn = React.createClass({

  displayName: 'SimpleDataTableColumn',

  mixins: [InterfaceMixin('DataTableColumn')],

  propTypes: {
    name: React.PropTypes.string, // field key
    title: React.PropTypes.string, // human-readable field name (to override schema)
    schema: React.PropTypes.object // schema for this column only (passed implicitly by SimpleDataTable)
  },
  render: function render () {
    throw new Error('SimpleDataTableColumn should never be rendered!')
  }
})

export default SimpleDataTableColumn