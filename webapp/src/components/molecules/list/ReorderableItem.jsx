import React from 'react'

export default React.createClass({
  propTypes: {
    item: React.PropTypes.object.isRequired
  },
  render: function () {
    let item = this.props.item
    return (
      <div key={item.id}>{item.name}
        <a className='clear-btn' onClick={item.removeFunction.bind(this, item.id)}>
          <i className='fa fa-times-circle'></i>
        </a>
      </div>
    )
  }
})

