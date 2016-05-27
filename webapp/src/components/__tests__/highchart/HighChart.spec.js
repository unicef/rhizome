import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import HighChart from '../../highchart/HighChart'

describe ('HighChart', () => {
  it ('exists', () => {
    expect (HighChart).to.exist
  })
  describe.skip ('.propTypes', () => {
    it ('exists', () => {
      expect (HighChart.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (HighChart.propTypes).to.have.all.keys('values', 'value', 'name', 'prefix', 'title', 'onChange', 'horizontal')
    })
  })
  describe.skip ('.getDefaultProps()', () => {
    it ('exists', () => {
      expect (HighChart.getDefaultProps).to.exist
    })
    it ('has proper keys and correct value', () => {
      expect (HighChart.getDefaultProps()).to.have.all.keys('prefix', 'horizontal')
      expect (HighChart.getDefaultProps().prefix).to.eq('')
      expect (HighChart.getDefaultProps().horizontal).to.be.false
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
      prefix: '',
      horizontal: false
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
