import _ from 'lodash'
import React, {Component, PropTypes} from 'react'
import Reflux from 'reflux'
import ReorderableIndicators from 'components/molecules/list/ReorderableIndicators'
import DropdownButton from 'components/atoms/buttons/DropdownButton'
import IndicatorSelect from 'components/atoms/select/IndicatorSelect'

class IndicatorMultiSelect extends Component {

  static propTypes = {
    indicators: PropTypes.shape({
      raw: PropTypes.array,
      list: PropTypes.array
    }).isRequired,
    selected_indicators: PropTypes.array,
    setIndicators: PropTypes.func,
    selectIndicator: PropTypes.func,
    deselectIndicator: PropTypes.func,
    clearSelectedIndicators: PropTypes.func,
    reorderIndicator: PropTypes.func,
    classes: PropTypes.string,
    multi: PropTypes.bool,
    filterByFormat: PropTypes.bool,
    avoidBooleans: PropTypes.bool,
    withColors: PropTypes.bool,
  }

  static defaultProps = {
    filterByFormat: true,
    withColors: true,
    avoidBooleans: false,
    multi: false,
    selected_indicators: []
  }

  getAvailableIndicators () {
    const selected_ids = this.props.selected_indicators.map(indicator => indicator.id)
    const first_indicator = this.props.selected_indicators[0]
    let indicators = []
    this.props.indicators.list.forEach(indicator_group => {
      let group = Object.assign({}, indicator_group)
      if (this.props.multi && this.props.filterByFormat && first_indicator) {
        // Filter out indicators of a different data_format from the dropdown menu
        // group.children = group.children.filter(item => first_indicator.data_format === item.data_format)
      }
      group.children = this.markDisabledIndicators(group.children, selected_ids)
      indicators.push(group)
    })
    return indicators.filter(indicator_group => indicator_group.children.length > 0)
  }

  markDisabledIndicators (items, selected_ids) {
    items.forEach(item => {
      item.disabled = selected_ids.indexOf(item.id) > -1
      if (item.children && item.children.length > 0) {
        this.markDisabledIndicators(item.children, selected_ids)
      }
    })
    return items
  }

  render () {
    const props = this.props
    const raw_indicators = props.indicators.raw || []
    const available_indicators = this.getAvailableIndicators()
    if (props.multi) {
      return (
        <form className={props.classes}>
          <h3 style={{marginBottom: '.1rem'}}>Indicators
            <DropdownButton
              items={available_indicators}
              sendValue={this.props.selectIndicator}
              item_plural_name='Indicators'
              style='icon-button right pad-right'
              icon='fa-plus'
            />
          </h3>
          {
            props.withColors
            ? <ReorderableIndicators {...props}/>
            : (
              <ReorderableList items={props.selected_indicators} removeItem={props.deselectIndicator} dragItem={props.reorderIndicator} />
            )
          }
          { props.selected_indicators.length > 1 ? <a className='remove-filters-link' onClick={props.clearSelectedIndicators}>Remove All </a> : '' }
        </form>
      )
    } else {
      const selected_indicator = _.isEmpty(this.props.selected_indicators) ? {name: 'Select Indicator'} : this.props.selected_indicators[0]
      return (
        <form className={props.classes}>
          <h3>Indicator</h3>
          <DropdownButton
            items={available_indicators}
            sendValue={this.props.setIndicators}
            item_plural_name='Indicators'
            style='dropdown-list'
            text={selected_indicator.short_name || selected_indicator.name}
          />
        </form>
      )
    }
  }
}

export default IndicatorMultiSelect
