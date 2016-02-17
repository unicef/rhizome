import _ from 'lodash'
import React from 'react/addons'
import InterfaceMixin from './../InterfaceMixin'

let FilterPanel = React.createClass({
  displayName: 'FilterPanel',

  mixins: [InterfaceMixin('Datascope', 'DatascopeFilter')],

  propTypes: {
    filter: React.PropTypes.objectOf(React.PropTypes.object),
    fields: React.PropTypes.array,
    schema: React.PropTypes.object,
    children: React.PropTypes.array,
    onChangeFilter: React.PropTypes.fun
  },

  getDefaultProps: function () {
    return {
      filter: {},
      schema: {},
      testing: 4
    }
  },

  onChangeFilterInput: function (key, filterObj) {
    this.props.onChangeFilter(key, filterObj)
  },

  recursiveCloneChildren: function (children) {
    let _this = this

    return React.Children.map(children, function (child) {
      if (!_.isObject(child)) return child

      let childProps = {}
      let isFilter = child.props && child.props.name
      if (isFilter) {
        let childKey = child.props.name
        let propSchemas = _this.props.schema.items.properties
        childProps = {
          schema: propSchemas[childKey],
          filter: _this.props.filter[childKey],
          onChange: _this.onChangeFilterInput.bind(_this, childKey)
        }
      }

      if (child.props.children) childProps.children = _this.recursiveCloneChildren(child.props.children)
      return React.cloneElement(child, childProps)
    })
  },

  render: function () {
    return React.createElement(
      'div',
      { className: 'datascope-filter-panel' },
      this.recursiveCloneChildren(this.props.children)
      )
  }
})

export default FilterPanel
