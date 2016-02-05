import React from 'react'
import _ from 'lodash'

import IndicatorDropdownMenu from 'component/dropdown-menus/IndicatorDropdownMenu.jsx'
import MapAxisChooser from '../MapAxisChooser.jsx'
import api from 'data/api'

import ChartWizardActions from 'actions/ChartWizardActions'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'

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
      <div className='chart-wizard__options chart-wizard__options--general'>
        <p className='chart-wizard__para'>You may choose additional indicators now.</p>
        <h4>Color Axis</h4>
        <ul className='list'>
          <li>{colorIndicator && colorIndicator.name}</li>
        </ul>
        <h4>Bubble Axis</h4>
        <IndicatorDropdownMenu
          text={bubbleIndicator ? bubbleIndicator.name : 'Add Indicators'}
          icon='fa-plus'
          indicators={intIndicators}
          sendValue={ChartWizardActions.changeYAxis}/>
        <h4>Gradient Axis</h4>
        <IndicatorDropdownMenu
          text={gradientIndicator ? gradientIndicator.name : 'Add Indicators'}
          icon='fa-plus'
          indicators={boolIndicators}
          sendValue={ChartWizardActions.changeZAxis}/>

        <p className='chart-wizard__para'>You may also change additional chart settings.</p>
        <MapAxisChooser colorFormatValue={this.props.xFormatValue}
                        onColorFormatChange={ChartWizardActions.changeXFormatRadio}
                        formatValues={builderDefinitions.formats}/>
      </div>
    )
  }
}
