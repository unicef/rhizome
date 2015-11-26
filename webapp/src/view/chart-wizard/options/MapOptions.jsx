import React from 'react'
import _ from 'lodash'
import List from 'component/list/List.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'
import MapAxisChooser from '../MapAxisChooser.jsx'
import PalettePicker from '../PalettePicker.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'

export default class GeneralOptions extends React.Component {
  constructor(props) {
    super(props)
  }

  static defaultProps = {
    indicatorList: [],
    indicatorSelected: [],
    groupByValue: 0,
    locationLevelValue: 0,
    yFormatValue: 0,
    palette: ''
  }


  filterIndicatorByType = (sourceList, indicatorType) => {
    if (!sourceList || !sourceList.length) {
      return sourceList
    }

    let indicatorList = _.cloneDeep(sourceList)
    let virtualRoot = {noValue: true, parentNode: null, empty: false, title: 'Virtual Root', children: indicatorList}
    indicatorList.forEach(item => item.parentNode = virtualRoot)

    let process = function (parent) {
      let children = parent.children

      if (children && children.length) {
        children.forEach(process)

        if (!children.some(item => !item.empty)) {
          parent.empty = true
        }
      } else {
        if (parent.noValue) {
          parent.empty = true
        }
        else{
          if (parent.data_format !== indicatorType) {
            if(parent.parentNode) {
              parent.parentNode.children.splice(parent.parentNode.children.indexOf(parent), 1)
            }
          }
        }
      }

      if (parent.empty && parent.parentNode) {
        parent.parentNode.children.splice(parent.parentNode.children.indexOf(parent), 1)
      }
    }

    process(virtualRoot)
    return virtualRoot.children
  }
  
  render() {
    return (
      <div className='chart-wizard__options chart-wizard__options--general'>
        <p className='chart-wizard__para'>You may choose additional indicators now.</p>
        <h4>Color Axis</h4>
        <ul className='list'>
          <li>{this.props.indicatorSelected[0] && this.props.indicatorSelected[0].name}</li>
        </ul>
        <h4>Bubble Axis</h4>
        <IndicatorDropdownMenu
          text={this.props.indicatorSelected[1] ? this.props.indicatorSelected[1].name : 'Add Indicators'}
          icon='fa-plus'
          indicators={this.filterIndicatorByType(this.props.indicatorList, 'int')}
          sendValue={ChartWizardActions.changeYAxis}/>
        <h4>Gradient Axis</h4>
        <IndicatorDropdownMenu
          text={this.props.indicatorSelected[2] ? this.props.indicatorSelected[2].name : 'Add Indicators'}
          icon='fa-plus'
          indicators={this.filterIndicatorByType(this.props.indicatorList, 'bool')}
          sendValue={ChartWizardActions.changeZAxis}/>

        <p className='chart-wizard__para'>You may also change additional chart settings.</p>
        <MapAxisChooser colorFormatValue={this.props.xFormatValue}
                        onColorFormatChange={ChartWizardActions.changeXFormatRadio}
                        formatValues={builderDefinitions.formats}/>
        <PalettePicker value={this.props.palette} onChange={ChartWizardActions.changePalette}/>
      </div>
    )
  }
}
