import React from 'react'
import IconButton from 'components/atoms/IconButton'

export default React.createClass({
  propTypes: {
    items: React.PropTypes.arrayOf(React.PropTypes.object).isRequired, // [{id:1,title:'abc'},...]
    removeItem: React.PropTypes.func.isRequired
  },
  render: function () {
    var listItems = this.props.items.map(item => {
      return (
        <li className='animated fadeInDown' key={item.id}>{item.name}
          <IconButton className='clear-btn' onClick={() => this.props.removeItem(item.id)} icon='fa-times-circle'/>
        </li>
      )
    })
    return <ul className='list'>{listItems}</ul>
  }
})
