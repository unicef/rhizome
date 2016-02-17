import _ from 'lodash'
import React from 'react/addons'

let RadioGroup = React.createClass({
  displayName: 'RadioGroup',

  propTypes: {
    children: React.PropTypes.array
  },

  render: function () {
    let _this = this

    return React.createElement(
      'div',
      _.omit(this.props, 'onChange'),
      React.Children.map(this.props.children, child => {
        let propsToPass = _.pick(_this.props, 'name')
        propsToPass.checked = _this.props.value !== null && _this.props.value === child.props.value
        propsToPass.onClick = _this.props.onChange.bind(null, child.props.value)
        return React.cloneElement(child, propsToPass)
      })
      )
  }
})

export default RadioGroup
