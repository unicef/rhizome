import React from 'react'

let UserAccount = React.createClass({
  propTypes: {
    userId: React.PropTypes.number
  },

  render: function () {
    return (
      <div>
        this is create UserAccount page and can get user_id : {this.props.userId}
      </div>
    )
  }
})

export default UserAccount
