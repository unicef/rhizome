import React from 'react'

export default React.createClass({
  propTypes: {
    items: React.PropTypes.arrayOf(React.PropTypes.object).isRequired, // [{id:1,title:'abc'},...]
    removeItem: React.PropTypes.func.isRequired
  },
  render: function () {
    var listItems = this.props.items.map(item => {
      return (<li className='animated slideInRight' key={item.id}>{item.name}
            <a
            className='clear-btn'
            onClick={this.props.removeItem.bind(this, item.id)}>
              <i className='fa fa-times-circle'></i>
            </a>
          </li>)
    })
    return <ul className='list'>{listItems}</ul>
  }
})
