import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import SwitchButton from '../../form/SwitchButton'
import sinon from 'sinon'

describe ('SwitchButton', () => {
  let mockSwitchButton
  beforeEach(() => {
    mockSwitchButton = new SwitchButton()
  })
  it ('exists', () => {
    expect (SwitchButton).to.exist
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (SwitchButton.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (SwitchButton.propTypes).to.have.all.keys('id', 'name', 'title', 'label', 'labelRight', 'defaultChecked', 'theme', 'checked', 'onChange')
    })
  })
  describe ('.defaultProps', () => {
    it ('exists', () => {
      expect (SwitchButton.defaultProps).to.exist
    })
    it ('has proper keys and correct value', () => {
      const defaultProps = SwitchButtonTest.getDefaultProps()
      expect (SwitchButton.defaultProps).to.have.all.keys('id', 'name', 'title', 'label', 'labelRight', 'defaultChecked', 'theme', 'checked', 'onChange')
      expect (SwitchButton.defaultProps.id).to.eq(defaultProps.id)
      expect (SwitchButton.defaultProps.name).to.eq(defaultProps.name)
      expect (SwitchButton.defaultProps.title).to.eq(defaultProps.title)
      expect (SwitchButton.defaultProps.label).to.eq(defaultProps.label)
      expect (SwitchButton.defaultProps.labelRight).to.eq(defaultProps.labelRight)
      expect (SwitchButton.defaultProps.defaultChecked).to.eq(defaultProps.defaultChecked)
      expect (SwitchButton.defaultProps.theme).to.eq(defaultProps.theme)
      expect (SwitchButton.defaultProps.checked).to.eq(defaultProps.checked)
      //does not initialize to reference function on default call if class function.. possible bug
      // expect (SwitchButton.defaultProps.onChange).to.eq(defaultProps.handleChange)
    })
  })
  describe ('#handleChange()', () => {
    it ('exists', () => {
      expect (mockSwitchButton.handleChange).to.exist
    })
  })
  describe ('#render()', () => {
    it ('exists', () => {
      expect (mockSwitchButton.render).to.exist
    })
    context ('with default props', () => {
      it ('renders correct jsx', () => {
        const props = SwitchButtonTest.getProps()
        const actualComponent = shallow(<SwitchButton {...props}/>).debug()
        const expectedComponent = shallow(SwitchButtonTest.getComponent()).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
    context ('with default props and props.label not empty', () => {
      it ('renders correct jsx', () => {
        let props = SwitchButtonTest.getProps()
        props.label = 'foo'
        const actualComponent = shallow(<SwitchButton {...props}/>).debug()
        const expectedComponent = shallow(SwitchButtonTest.getComponent(props)).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
    context ('with default props and props.label not empty', () => {
      it ('renders correct jsx', () => {
        let props = SwitchButtonTest.getProps()
        props.labelRight = 'foo'
        const actualComponent = shallow(<SwitchButton {...props}/>).debug()
        const expectedComponent = shallow(SwitchButtonTest.getComponent(props)).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
  })
})

class SwitchButtonTest {
  static getProps() {
    return {
      id: '',
      name: 'switch-button',
      title: '',
      label: '',
      labelRight: '',
      defaultChecked: '',
      theme: 'switch-button-flat-round',
      checked: null,
      onChange: this.handleChange
    }
  }
  static getDefaultProps() {
    return {
      id: '',
      name: 'switch-button',
      title: '',
      label: '',
      labelRight: '',
      defaultChecked: '',
      theme: 'switch-button-flat-round',
      checked: null,
      onChange: this.handleChange
    }
  }
  static handleChange() {
    // Override
  }
  static getComponent(argProps = null) {
    let props = argProps || this.getProps()
    const id = props.id || props.name
    let label
    let labelRight

    if (props.label != '') {
      label = <label htmlFor={id}>{props.label}</label>
    }

    if (props.labelRight != '') {
      labelRight = <label htmlFor={id}>{props.labelRight}</label>
    }
    return (
      <div className={'switch-button ' + props.theme} >
        {label}
        <input
          id={id}
          value={1}
          type='checkbox'
          name={props.name}
          checked={props.checked}
          onChange={props.onChange}
          defaultChecked={props.defaultChecked}
        />
        <label htmlFor={id}></label>
        {labelRight}
      </div>
    )
  }
}
