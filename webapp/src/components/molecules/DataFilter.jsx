import React from 'react'

import ExpandableSection from 'components/molecules/ExpandableSection'
import DropdownButton from 'components/atoms/button/DropdownButton'
import ReorderableList from 'components/molecules/list/ReorderableList'
import List from 'components/molecules/list/List'

let DataFilter = React.createClass({

  propTypes: {
    items: React.PropTypes.array.isRequired,
    addItem: React.PropTypes.func.isRequired,
    removeItem: React.PropTypes.func.isRequired,
    reorderItem: React.PropTypes.func,
    selected_items: React.PropTypes.array,
    item_plural_name: React.PropTypes.string,
    text: React.PropTypes.string,
    style: React.PropTypes.string,
    icon: React.PropTypes.string,
    reorderable: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      items: [],
      style: 'databrowser__button',
      reorderable: false
    }
  },

  render: function () {
    let selected_item_list = <List items={this.props.selected_items} removeItem={this.props.removeItem} />

    if (this.props.reorderable) {
      selected_item_list = <ReorderableList items={this.props.selected_items} removeItem={this.props.removeItem} dragItem={this.props.reorderItem}/>
    }

    return (
      <ExpandableSection title={this.props.item_plural_name} refer='preview'>
        <DropdownButton items={this.props.items} sendValue={this.props.addItem} item_plural_name={this.props.item_plural_name} text={this.props.text} style={this.props.style} icon={this.props.icon}/>
        {selected_item_list}
      </ExpandableSection>
    )
  }
})

export default DataFilter
