import _ from 'lodash'
import React from 'react/addons'
import moment from 'moment'
import numeral from 'numeral'
import InterfaceMixin from './../InterfaceMixin'

// mostly for debugging, not fleshed out

let DataList = React.createClass({
  displayName: 'DataList',

  mixins: [InterfaceMixin('Datascope', 'DatascopeSearch', 'DatascopeSort', 'DatascopeFilter')],

  propTypes: {
    data: React.PropTypes.array.isRequired
  },

  render: function () {
    let _this = this

    return React.createElement(
      'div',
      null,
      this.props.data.map(d => {
        return _.map(_this.props.orderedFields, function (field) {
          return React.createElement(
            'div',
            null,
            React.createElement(
              'strong',
              null,
              field.title,
              ': '
              ),
            field.renderer(d[field.key], field, { moment: moment, numeral: numeral })
            )
        }).concat(React.createElement('hr', null))
      })
      )
  }
})

export default DataList
