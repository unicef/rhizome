import React from 'react'
import Reorderable from 'react-reorder'
import ReorderableItem from 'components/molecules/list/ReorderableItem.jsx'

export default React.createClass({
  propTypes: {
    items: React.PropTypes.arrayOf(React.PropTypes.object).isRequired, // [{id:1,title:'abc'},...]
    removeItem: React.PropTypes.func,
    dragItem: React.PropTypes.func
  },
  rearrangeItems: function (event, itemThatHasBeenMoved, itemsPreviousIndex, itemsNewIndex, reorderedArray) {
    this.props.dragItem(reorderedArray)
  },
  render: function () {
    // Attach the remove function to each item for use in the item template
    let items = this.props.items.map(item => {
      item.removeFunction = this.props.removeItem
      return item
    })

    return <Reorderable
      itemKey='id'
      lock='horizontal'
      holdTime='100'
      template={ReorderableItem}
      callback={this.rearrangeItems}
      listClass='reorderable-list'
      itemClass='reorderable-item animated fadeInDown'
      removeItem={this.props.removeItem}
      disableReorder={false}
      list={items}/>
  }
})
