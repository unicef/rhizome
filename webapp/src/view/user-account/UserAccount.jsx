import React from 'react'

import UserGroup from 'component/UserGroup.jsx'

let UserAccount = React.createClass({
  propTypes: {
    userId: React.PropTypes.number
  },

  render: function () {
    return (
      <div>
        <div className='row' style={{marginBottom: '15px'}}>
          <div className='columns small-4 left-box'>
            <h4>Roles</h4>
            <div className='label-box'>
            Roles determine what functions this user can perform and which indicators for which they can enter data. All users can consume data (see dashboards and explore with data browser), as long as they have locational permission to do so
            </div>
          </div>
          <UserGroup userId={this.props.userId}/>
        </div>
      </div>
    )
  }
})

export default UserAccount
