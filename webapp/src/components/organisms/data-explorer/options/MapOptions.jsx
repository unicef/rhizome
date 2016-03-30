import React from 'react'
import _ from 'lodash'

import DropdownMenu from 'components/molecules/menus/DropdownMenu.jsx'
import MapAxisChooser from '../MapAxisChooser.jsx'
import api from 'data/api'

import DataExplorerActions from 'actions/DataExplorerActions'
import builderDefinitions from 'components/molecules/charts_d3/utils/builderDefinitions'

export default class GeneralOptions extends React.Component {
  constructor (props) {
    super(props)
  }

  static propTypes = {
    indicatorList: React.PropTypes.array,
    indicatorSelected: React.PropTypes.array,
    groupByValue: React.PropTypes.number,
    locationLevelValue: React.PropTypes.number,
    xFormatValue: React.PropTypes.number,
    yFormatValue: React.PropTypes.number,
    rawIndicators: React.PropTypes.object,
    rawTags: React.PropTypes.object
  }

  static defaultProps = {
    indicatorList: [],
    indicatorSelected: [],
    groupByValue: 0,
    locationLevelValue: 0,
    xFormatValue: 0,
    yFormatValue: 0,
    rawIndicators: null,
    rawTags: null
  }

  render () {
    let intIndicators = _.sortBy(api.buildIndicatorsTree(this.props.rawIndicators.objects, this.props.rawTags.objects, true, true, 'int'), 'title')
    let boolIndicators = _.sortBy(api.buildIndicatorsTree(this.props.rawIndicators.objects, this.props.rawTags.objects, true, true, 'bool'), 'title')
    let [colorIndicator, bubbleIndicator, gradientIndicator] = this.props.indicatorSelected
    return (
      <div className='data-explorer__options data-explorer__options--general'>
        <p className='data-explorer__para'>You may choose additional indicators now.</p>
        <h4>Color Axis</h4>
        <ul className='list'>
          <li>{colorIndicator && colorIndicator.name}</li>
        </ul>
        <h4>Bubble Axis</h4>
        <DropdownMenu
          items={intIndicators}
          sendValue={DataExplorerActions.changeYAxis}
          item_plural_name='Indicators'
          text={bubbleIndicator ? bubbleIndicator.name : 'Add Indicators'}
          icon='fa-plus'/>
        <h4>Gradient Axis</h4>
        <DropdownMenu
          items={boolIndicators}
          sendValue={DataExplorerActions.changeZAxis}
          item_plural_name='Indicators'
          text={bubbleIndicator ? bubbleIndicator.name : 'Add Indicators'}
          icon='fa-plus'/>
        <p className='data-explorer__para'>You may also change additional chart settings.</p>
        <MapAxisChooser colorFormatValue={this.props.xFormatValue}
                        onColorFormatChange={DataExplorerActions.changeXFormatRadio}
                        formatValues={builderDefinitions.formats}/>
      </div>
    )
  }
}
