import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import RadioGroup from '../../form/RadioGroup'
import sinon from 'sinon'

describe ('RadioGroup', () => {
  it ('exists', () => {
    expect (RadioGroup).to.exist
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (RadioGroup.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (RadioGroup.propTypes).to.have.all.keys('values', 'value', 'name', 'prefix', 'title', 'onChange', 'horizontal')
    })
  })
  describe ('.getDefaultProps()', () => {
    it ('exists', () => {
      expect (RadioGroup.getDefaultProps).to.exist
    })
    it ('has proper keys and correct value', () => {
      expect (RadioGroup.getDefaultProps()).to.have.all.keys('prefix', 'horizontal')
      expect (RadioGroup.getDefaultProps().prefix).to.eq('')
      expect (RadioGroup.getDefaultProps().horizontal).to.be.false
    })
  })
  describe ('#render()', () => {
    it ('exists', () => {
      const mockDropdownMenuItem = new RadioGroup()
      expect (mockDropdownMenuItem.render).to.exist
    })
    it ('renders correct jsx', () => {
      const props = RadioGroupTest.getProps()
      const actualComponent = shallow(<RadioGroup {...props}/>).debug()
      const expectedComponent = shallow(RadioGroupTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
  })
})

class RadioGroupTest {
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
