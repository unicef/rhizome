import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import _ from 'lodash'
import DropdownMenu from '../../dropdown/DropdownMenu'
import DropdownMenuSearch from '../../dropdown/DropdownMenuSearch'
import dom from 'utilities/dom'
import sinon from 'sinon'

describe ('DropdownMenu', () => {
  let mockDropdownMenu
  beforeEach (() => {
    mockDropdownMenu = new DropdownMenu(DropdownMenuTest.getDefaultProps())
  })
  it ('exists', () => {
    expect (DropdownMenu).to.exist
  })
  it ('extends react component', () => {
    expect (mockDropdownMenu instanceof React.Component).to.be.true
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (DropdownMenu.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (DropdownMenu.propTypes).to.have.all.keys('onSearch', 'onBlur', 'searchable', 'x', 'y', 'children', 'search')
    })
  })
  describe ('#defaultProps', () => {
    it ('exists', () => {
      expect (DropdownMenu.defaultProps).to.exist
    })
    it ('returns specified properties', () => {
      const key = DropdownMenu.defaultProps
      expect (key).to.have.all.keys('onSearch', 'onBlur', 'searchable', 'x', 'y')
    })
    it ('has correct initial values', () => {
      const expectedProps = DropdownMenuTest.getDefaultProps()
      const actualProps = DropdownMenu.defaultProps
      expect (actualProps.onSearch).to.eq(expectedProps.onSearch)
      expect (actualProps.onBlur).to.eq(expectedProps.onBlur)
      expect (actualProps.searchable).to.eq(expectedProps.searchable)
      expect (actualProps.x).to.eq(expectedProps.x)
      expect (actualProps.y).to.eq(expectedProps.y)
    })
  })
  describe ('#constructor()', () => {
    it ('has a constructor which has 1 parameter', () => {
      expect (DropdownMenu.constructor).to.exist.and.have.lengthOf(1)
    })
    context ('given an argument', () => {
      const props = { foo: 'bar', bar: 'foo' }
      it ('props passed should also be passed up to super', () => {
        const spy = sinon.spy(React.Component.prototype, 'constructor')
        const spyMockDropdownMenu = new DropdownMenu(props)
        expect (spy.called).to.be.true
        expect (spy.calledWith(props)).to.be.true
        React.Component.prototype.constructor.restore()
      })
      it ('initializes instance variable `state`', () => {
        mockDropdownMenu = new DropdownMenu(props)
        const state = DropdownMenuTest.getState()
        expect (mockDropdownMenu.state.maxHeight).to.eq(state.maxHeight)
        expect (mockDropdownMenu.state.marginLeft).to.eq(state.marginLeft)
        expect (mockDropdownMenu.state.orientation).to.eq(state.orientation)
        expect (mockDropdownMenu.state.pattern).to.eq(state.pattern)
      })
    })
  })
  describe ('#_onResize()', () => {

  })
  describe ('#componentWillUnmount()', () => {

  })
  describe ('#componentDidMount()', () => {

  })
  describe ('#componentDidUpdate()', () => {

  })
  describe ('#shouldComponentUpdate()', () => {

  })
  describe ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<DropdownMenu {...DropdownMenuTest.getProps()}/>)
      expectedComponent = DropdownMenuTest.mockComponent()
    })
    it.skip ('renders correct components', () => {
      expect (wrapper.equals(expectedComponent)).to.be.true
    })
    it ('contains 4 div\'s', () => {
      expect (wrapper.find('div')).to.have.length(4)
    })
    it.skip ('simulates onBlur events for outter most div', () => {
      let reactPrototype = DropdownMenu.prototype
      let spy = sinon.spy(reactPrototype, 'onBlur')
      let spyMockDropdownMenu = new DropdownMenu()
      spyMockDropdownMenu.onBlur()
      expect (spy.calledOnce).to.be.true
      reactPrototype.onBlur.restore()
    })
  })
})
class DropdownMenuTest {
  static getProps() {
    //update working variable if isWorking is switched to true
    return {
      onSearch: () => null,
      onBlur: () => null,
      searchable: false,
      x: 11,
      y: 22,
      children: [],
      search: ['', false]
    }
  }
  static getDefaultProps() {
    return {
      onSearch: _.noop,
      onBlur: _.noop,
      searchable: false,
      x: 0,
      y: 0
    }
  }
  static getState() {
    return {
      maxHeight: 'none',
      marginLeft: 0,
      orientation: 'center',
      pattern: ''
    }
  }
  static mockComponent() {
    const props = this.getProps()
    const state = this.getState()
    let itemlistStyle = { maxHeight: state.maxHeight }
    let containerStyle = { marginLeft: state.marginLeft }
    let position = {
      position: 'absolute',
      left: props.x,
      top: props.y
    }

    let search = props.searchable ? (<DropdownMenuSearch onChange={props.onSearch} onBlur={this.onBlur} />) : null

    return (
      <div className='menu' style={position} tabIndex='-1' onBlur={this.onBlur}>
        <div className={state.orientation + ' container'}
          style={containerStyle}
          ref='menu'>

          <div className='background'>
            <div className='arrow'></div>
            {search}
            <ul ref='itemlist' style={itemlistStyle}>
              {props.children}
            </ul>
          </div>

        </div>
      </div>
    )
  }
}