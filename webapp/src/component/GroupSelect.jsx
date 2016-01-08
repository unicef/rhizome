import React from 'react'
import api from 'data/api'

let UserGroup = React.createClass({
  propTypes: {
    data: React.PropTypes.object,
    userId: React.PropTypes.number
  },

  getInitialState: function () {
    return {
      groupActive: this.props.data.active
    }
  },

  changeSelect: function () {
    if (!this.state.groupActive) {
      api.post_user_permission({'user_id': this.props.userId, 'group_id': this.props.data.id})
      this.setState({groupActive: true})
    } else {
      api.delete_user_permission({'user_id': this.props.userId, 'group_id': this.props.data.id})
      this.setState({groupActive: false})
    }
  },

  render: function () {
    return (
        <input type='checkbox'
          checked={this.state.groupActive}
          onClick={this.changeSelect}>
          <span>{this.props.data.name}</span>
        </input>
    )
  }
})

export default UserGroup
