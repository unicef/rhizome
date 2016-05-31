import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import CheckBoxGroup from '../../form/CheckBoxGroup'
import sinon from 'sinon'

class CheckBoxGroupTest {
  static getProps() {
    return {
      values: [{check: {value: 1, title: 'foo'}}, {check: {value: 2, title: 'bar'}}, {check: {value: 3, title: 'foobar'}}],
      value: '1',
      name: 'foo',
      prefix: '',
      title: 'bar',
      onChange: () => null
    }
  }
  static getComponent() {
    const props = this.getProps()
    let checkboxes = props.values.map((check, index) => {
      return (
        <div key={check.value}>
          <input type='checkbox' name={props.name} id={`${props.prefix}${check.value}`}
            value={check.value}
            checked={props.value.indexOf(index) >= 0 ? 'checked' : false}
            onChange={props.onChange.bind(null, index)} />
          <label htmlFor={`${props.prefix}${check.value}`}>{check.title}</label>
        </div>
      )
    })
    return (
      <div className='checkbox-group'>
        <h4>{props.title}</h4>
        {checkboxes}
      </div>
    )
  }
}

describe ('CheckBoxGroup', () => {
  it ('exists', () => {
    expect (CheckBoxGroup).to.exist
  })
  describe ('.constructor()', () => {
    it ('has a constructor which has 1 parameter', () => {
      expect (CheckBoxGroup.constructor).to.exist.and.have.lengthOf(1)
    })
    context ('given an argument', () => {
      const props = CheckBoxGroupTest.getProps()
      it ('props passed should also be passed up to super', () => {
        const spy = sinon.spy(React.Component.prototype, 'constructor')
        const spyMockDropdown = new CheckBoxGroup(props)
        React.Component.prototype.constructor.restore()
        expect (spy.called).to.be.true
        expect (spy.calledWith(props)).to.be.true
      })
    })
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (CheckBoxGroup.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (CheckBoxGroup.propTypes).to.have.all.keys('values', 'value', 'name', 'prefix', 'title', 'onChange')
    })
  })
  describe ('.defaultProps', () => {
    it ('exists', () => {
      expect (CheckBoxGroup.defaultProps).to.exist
    })
    it ('has proper keys and correct value', () => {
      expect (CheckBoxGroup.defaultProps).to.have.all.keys('prefix')
      expect (CheckBoxGroup.defaultProps.prefix).to.eq('')
    })
  })
  describe ('#render()', () => {
    it ('exists', () => {
      const mockDropdownMenuItem = new CheckBoxGroup()
      expect (mockDropdownMenuItem.render).to.exist
    })
    it ('renders correct jsx', () => {
      const props = CheckBoxGroupTest.getProps()
      const actualComponent = shallow(<CheckBoxGroup {...props}/>).debug()
      const expectedComponent = shallow(CheckBoxGroupTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
  })
})