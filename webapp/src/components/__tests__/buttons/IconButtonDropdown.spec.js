import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import IconButtonDropdown from '../../button/IconButtonDropdown'
import IconButton from '../../button/IconButton'
import Dropdown from '../../dropdown/Dropdown'
import sinon from 'sinon'

describe ('IconButtonDropdown', () => {
  let mockIconButtonDropdown
  beforeEach (() => {
    mockIconButtonDropdown = new IconButtonDropdown(IconButtonDropdownTest.getDefaultProps())
  })
  it ('exists', () => {
    expect (IconButtonDropdown).to.exist
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (IconButtonDropdown.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (IconButtonDropdown.propTypes).to.have.all.keys('icon', 'color', 'text', 'className', 'onSearch', 'searchable')
    })
  })
  describe ('#getDefaultProps()', () => {
    it ('exists', () => {
      expect (IconButtonDropdown.defaultProps).to.exist
    })
    it ('returns specified properties', () => {
      expect (IconButtonDropdown.defaultProps).to.have.all.keys('icon', 'onSearch')
    })
    it ('has correct initial values', () => {
      const expectedProps = IconButtonDropdownTest.getDefaultProps()
      const actualProps = IconButtonDropdown.defaultProps
      expect (actualProps.onSearch()).to.be.null
      expect (actualProps.icon).to.eq(expectedProps.icon)
    })
  })
  describe ('#componentWillReceiveProps()', () => {
    it ('exists', () => {
      expect (mockIconButtonDropdown.componentWillReceiveProps).to.exist
    })
    context ('given a nextProps argument with text that does not match current props.text', () => {
      it ('sets the state of `open`', () => {
        const spy = sinon.spy(IconButtonDropdown.prototype, 'setState')
        let mockIconButtonDropdownWithText = new IconButtonDropdown({ text: '' })
        mockIconButtonDropdownWithText.componentWillReceiveProps({ text: 'foo' })
        expect (spy.calledOnce).to.be.true
        IconButtonDropdown.prototype.setState.restore()
      })
      it ('sets the state of `open` to false', () => {
        const spy = sinon.spy(IconButtonDropdown.prototype, 'setState')
        let mockIconButtonDropdownWithText = new IconButtonDropdown({ text: '' })
        mockIconButtonDropdownWithText.componentWillReceiveProps({ text: 'foo' })
        expect (spy.calledWith({ open: false })).to.be.true
        IconButtonDropdown.prototype.setState.restore()
      })
    })
    context ('given a nextProps argument with text that matches current props.text', () => {
      it ('does not set state of anything', () => {
        const spy = sinon.spy(IconButtonDropdown.prototype, 'setState')
        let mockIconButtonDropdownWithText = new IconButtonDropdown({ text: '' })
        mockIconButtonDropdownWithText.componentWillReceiveProps({ text: '' })
        expect (spy.called).to.be.false
        IconButtonDropdown.prototype.setState.restore()
      })
    })
  })
  describe ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<IconButtonDropdown {...IconButtonDropdownTest.getProps()}/>)
      expectedComponent = IconButtonDropdownTest.mockComponent()
    })
    it.skip ('renders correct components', () => {
      expect (wrapper.equals(expectedComponent)).to.be.true
    })
    it ('contains a button', () => {
      expect (wrapper.find('IconButton')).to.have.length(1)
    })
    it.skip ('simulates click events', () => {
      let spy = sinon.spy(IconButtonDropdown.prototype, '_toggleMenu')
      wrapper = shallow(<IconButtonDropdown />)
      wrapper.find('IconButton').simulate('click')
      expect (spy.calledOnce).to.be.true
      IconButtonDropdown.prototype._toggleMenu.restore()
    })
  })
})
class IconButtonDropdownTest {
  static getProps() {
    //update working variable if isWorking is switched to true
    return {
      className: '',
      color: null,
      text: 'foo',
      icon: '',
      searchable: false,
      onSearch: () => null
    }
  }
  static getDefaultProps() {
    return {
      icon: 'fa-bars',
      onSearch: () => null
    }
  }
  _toggleMenu() {

  }
  static mockComponent() {
    const props = this.getProps()
    return (
      <IconButton {...props} onClick={this._toggleMenu}/>
    )
  }
}