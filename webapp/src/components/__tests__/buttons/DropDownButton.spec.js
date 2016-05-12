import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import DropdownButton from '../../button/DropdownButton'
import sinon from 'sinon'

describe ('DropdownButton', () => {
  let mockDropdownButton
  beforeEach (() => {
    mockDropdownButton = new DropdownButton()
  })
  it ('exists', () => {
    expect (DropdownButton).to.exist
  })
  describe ('.propTypes', () => {
    it ('is static and exists', () => {
      expect (DropdownButton.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (DropdownButton.propTypes).to.have.all.keys('items', 'sendValue', 'item_plural_name', 'text', 'style', 'icon', 'value_field', 'title_field', 'uniqueOnly', 'multi', 'grouped')
    })
    context ('if component is mounted it warns for required props', () => {
      let spy, wrapper
      beforeEach(() => {
        spy = sinon.spy(console, 'warn')
        wrapper = shallow(<DropdownButton />)
      })
      afterEach (() => {
        console.warn.restore()
      })
      it ('correct number of warnings', () => {
        expect (spy.calledTwice).to.be.true
      })
      it.skip ('warns with proper message', () => {
        expect (spy.calledWith('Warning: Failed propType: Required prop `items` was not specified in `DropdownButton`')).to.be.true
        expect (spy.calledWith('Warning: Failed propType: Required prop `sendValue` was not specified in `DropdownButton`')).to.be.true
      })
    })
  })
  describe ('#defaultProps', () => {
    it ('has specified properties', () => {
      expect (DropdownButton.defaultProps).to.have.all.keys('uniqueOnly', 'multi', 'grouped', 'value_field', 'title_field')
    })
    it ('has correct initial values', () => {
      const defaultProps = DropdownButtonTest.getDefaultProps()
      expect (DropdownButton.defaultProps.uniqueOnly).to.eq(defaultProps.uniqueOnly)
      expect (DropdownButton.defaultProps.multi).to.eq(defaultProps.multi)
      expect (DropdownButton.defaultProps.grouped).to.eq(defaultProps.grouped)
      expect (DropdownButton.defaultProps.value_field).to.eq(defaultProps.value_field)
      expect (DropdownButton.defaultProps.title_field).to.eq(defaultProps.title_field)
    })
  })
  describe ('#componentWillRecieveProps()', () => {
    it ('exists with 1 parameter', () => {
      expect (mockDropdownButton.componentWillReceiveProps).to.exist.and.have.lengthOf(1)
    })
    context ('if an argument is passed in', () => {
      it ('sets state of `open` to false', () => {
        const props = { text: 'bar' }
        const spyMockDropdownButton = new DropdownButton({ text: 'foo'})
        spyMockDropdownButton.componentWillReceiveProps(props)
        expect (spyMockDropdownButton.state.open).to.be.false
      })
      it ('sets state of `open`', () => {
        const props = { text: 'bar' }
        const spy = sinon.spy(DropdownButton.prototype, 'setState')
        const spyMockDropdownButton = new DropdownButton({ text: 'foo'})
        spyMockDropdownButton.componentWillReceiveProps(props)
        expect (spy.calledOnce).to.be.true
        DropdownButton.prototype.setState.restore()
      })
    })
  })
  describe ('#componentWillUpdate()', () => {
    const props = { items: [{title: 'foobar', value: '1'}], grouped: true, uniqueOnly: false }
    it ('exists with 2 arguments', () => {
      expect (mockDropdownButton.componentWillUpdate).to.exist.and.have.lengthOf(2)
    })
    context.skip ('when given 2 arguments and props.grouped is true', () => {
      it ('calls #_getGroupedMenuItemComponents()', () => {
        const spy = sinon.spy(DropdownButton.prototype, '_getGroupedMenuItemComponents')
        const spyMockDropdownButton = new DropdownButton({ grouped: true })
        spyMockDropdownButton.componentWillUpdate(props)
        expect (spy.calledOnce).to.be.true
        DropdownButton.prototype._getGroupedMenuItemComponents.restore()
      })
    })
    context.skip ('when given 2 arguments and props.grouped is false', () => {
      it ('calls #_getMenuItemComponents()', () => {
        const spy = sinon.spy(DropdownButton.prototype, '_getMenuItemComponents')
        const spyMockDropdownButton = new DropdownButton({ grouped: false })
        spyMockDropdownButton.componentWillUpdate(props)
        expect (spy.calledOnce).to.be.true
        DropdownButton.prototype._getMenuItemComponents.restore()
      })
    })
    context.skip ('when given 2 arguments', () => {
      it ('calls #_setPattern()', () => {
        const spy = sinon.spy(DropdownButton.prototype, '_setPattern')
        const spyMockDropdownButton = new DropdownButton(props)
        spyMockDropdownButton.componentWillUpdate(props)
        expect (spy.calledOnce).to.be.true
        DropdownButton.prototype._setPattern.restore()
      })
    })
  })
  describe.skip ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<DropdownButton {...DropdownButtonTest.getProps()}/>)
      expectedComponent = DropdownButtonTest.mockComponent()
    })
    it.skip ('renders correct components', () => {
      expect (wrapper.equals(expectedComponent)).to.eq(true)
    })
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    it.skip ('contains an inner component', () => {
      expect (wrapper.contains(DropdownButtonTest.mockInnerComponent())).to.eq(true)
    })
    it ('simulates click events', () => {
      let spy = sinon.spy(DropdownButton.prototype.__reactAutoBindMap, "_download")
      wrapper = shallow(<DropdownButton {...DropdownButtonTest.getProps()} />)
      wrapper.find('button').simulate('click')
      expect (spy.calledOnce).to.be.true
      spy.restore() //double check if this restores _download method
    })
  })
})
class DropdownButtonTest {
  static getProps() {
    //update working variable if isWorking is switched to true
    return {
      text: 'stuff',
      enable: true,
      classes: '',
      working: 'bar',
      cookieName: 'foo',
      onClick: () => {}
    }
  }
  static getDefaultProps() {
    return {
      uniqueOnly: false,
      multi: false,
      grouped: false,
      value_field: 'value',
      title_field: 'title'
    }
  }
  static getState() {
    return {
      uniqueOnly: false,
      multi: false,
      grouped: false,
      value_field: 'value',
      title_field: 'title'
    }
  }
  _download() {

  }
  static mockComponent() {
    const props = this.getProps()
    const state = this.getState()
    let text = state.isWorking ? props.working : props.text
    let classesString = props.enable && !state.isWorking ? 'button success expand ' : 'button success expand disabled '
    return (
      <button role='button'
        className={classesString + props.classes}
        onClick={this._download}>
        <i className='fa fa-fw fa-download' /> {text}
        <iframe width='0' height='0' className='hidden' src={state.url}></iframe>
      </button>
    )
  }
  static mockInnerComponent() {
    const props = this.getProps()
    const state = this.getState()
    let text = state.isWorking ? props.working : props.text
    let classesString = props.enable && !state.isWorking ? 'button success expand ' : 'button success expand disabled '
    //return needs to be fixed. div should be removed.
    return (
      <div>
        <i className='fa fa-fw fa-download' /> {text}
        <iframe width='0' height='0' className='hidden' src={state.url}></iframe>
      </div>
    )
  }
}