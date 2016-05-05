import React from 'react'
import Reorderable from 'react-reorder'
import ReorderableIndicator from 'components/molecules/list/ReorderableIndicator'

export default React.createClass({
  propTypes: {
    selected_indicators: React.PropTypes.arrayOf(React.PropTypes.object).isRequired, // [{id:1,title:'abc'},...]
    deselectIndicator: React.PropTypes.func,
    setIndicatorColor: React.PropTypes.func,
    reorderIndicator: React.PropTypes.func
  },
  rearrangeItems: function (event, itemThatHasBeenMoved, selected_indicatorsPreviousIndex, selected_indicatorsNewIndex, reorderedArray) {
    this.props.reorderIndicator(reorderedArray)
  },
  render: function () {
    // Attach the remove function to each item for use in the item template
    let selected_indicators = this.props.selected_indicators.map(item => {
      item.deselectIndicator = this.props.deselectIndicator
      item.setIndicatorColor = this.props.setIndicatorColor
      item.selectedColor = this.props.indicator_colors[item.id]
      return item
    })
    return <Reorderable
      itemKey='id'
      lock='horizontal'
      holdTime='100'
      template={ReorderableIndicator}
      callback={this.rearrangeItems}
      listClass='reorderable-list'
      itemClass='reorderable-item animated fadeInDown'
      removeItem={this.props.deselectIndicator}
      setIndicatorColor={this.props.setIndicatorColor}
      disableReorder={false}
      list={selected_indicators}/>
  }
})
