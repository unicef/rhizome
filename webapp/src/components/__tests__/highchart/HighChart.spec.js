import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import HighChart from '../../highchart/HighChart'
import Highcharts from 'highcharts'
import themes from 'components/highchart/themes'
import sinon from 'sinon'

class HighChartTest {
  static getProps() {
    return {
      values: [{check: {value: 1, title: 'foo'}}, {check: {value: 2, title: 'bar'}}, {check: {value: 3, title: 'foobar'}}],
      value: '1',
      name: 'foo',
      prefix: '',
      horizontal: false,
      title: 'bar',
      onChange: () => null
    }
  }
  static getDefaultProps () {
    return {
      isPureConfig: true
    }
  }
  static getComponent() {
    const props = this.getProps()
    const radios = props.values.map((radio, index) => {
      return (
        <div key={radio.value} className={props.horizontal ? 'horizontal' : null}>
          <input type='radio' name={props.name} id={`${props.prefix}${radio.value}`}
            value={radio.value}
            checked={props.value === radio.value ? 'checked' : false}
            onChange={() => props.onChange(radio.value)}
            />
          <label htmlFor={`${props.prefix}${radio.value}`}>{radio.title}</label>
        </div>
      )
    })
    return (
      <div className='radio-group-container'>
        <h4>{props.title}</h4>
        {radios}
      </div>
    )
  }
}

describe ('HighChart', () => {
  let mockHighChart
  beforeEach(() => {
    mockHighChart = shallow(<HighChart />).instance()
  })
  it ('exists', () => {
    expect (HighChart).to.exist
  })
  describe ('#constructor()', () => {
    it ('has a constructor which has 1 parameter', () => {
      expect (HighChart.constructor).to.exist.and.have.lengthOf(1)
    })
    context ('given an argument', () => {
      const props = HighChartTest.getProps()
      it ('props passed should also be passed up to super', () => {
        const spy = sinon.spy(React.Component.prototype, 'constructor')
        const spyMockDropdown = new HighChart(props)
        React.Component.prototype.constructor.restore()
        expect (spy.called).to.be.true
        expect (spy.calledWith(props)).to.be.true
      })
      it ('calls Highcharts.setOptions with correct argument', () => {
        const spy = sinon.spy(Highcharts, 'setOptions')
        const spyMockDropdown = new HighChart(props)
        Highcharts.setOptions.restore()
        expect (spy.called).to.be.true
        expect (spy.calledWith(themes.standard)).to.be.true
      })
    })
  })

  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (HighChart.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (HighChart.propTypes).to.have.all.keys('config', 'map', 'isPureConfig', 'neverReflow')
    })
  })
  describe ('.defaultProps', () => {
    it ('exists', () => {
      expect (HighChart.defaultProps).to.exist
    })
    it ('has proper keys and correct value', () => {
      const defaultProps = HighChartTest.getDefaultProps()
      expect (HighChart.defaultProps).to.have.all.keys('isPureConfig')
      expect (HighChart.defaultProps.isPureConfig).to.eq(defaultProps.isPureConfig)
    })
  })
  describe.skip ('componentDidMount', () => {
    it ('exists', () => {
      expect (mockHighChart.componentDidMount).to.exist
    })
    it ('calls renderChart()', () => {
      const spy = sinon.spy(mockHighChart, 'renderChart')
      mockHighChart.componentDidMount()
      mockHighChart.renderChart.restore()
      expect (spy.calledOnce).to.exist
    })
  })
  describe.skip ('#render()', () => {
    it ('exists', () => {
      const mockDropdownMenuItem = new HighChart()
      expect (mockDropdownMenuItem.render).to.exist
    })
    it ('renders correct jsx', () => {
      const props = HighChartTest.getProps()
      const actualComponent = shallow(<HighChart {...props}/>).debug()
      const expectedComponent = shallow(HighChartTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
  })
})