import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import Dropdown from '../../dropdown/Dropdown'
import sinon from 'sinon'

describe ('Dropdown', () => {
  let mockDropdown
  beforeEach (() => {
    mockDropdown = new Dropdown()
  })
  it ('exists', () => {
    expect (Dropdown).to.exist
  })
  it ('extends Component class of React', () => {
    expect (mockDropdown instanceof React.Component).to.be.true
  })
  describe ('.constructor()', () => {
    it ('has a constructor which has 1 parameter', () => {
      expect (Dropdown.constructor).to.exist.and.have.lengthOf(1)
    })
    context ('given an argument', () => {
      const props = { foo: 'bar', bar: 'foo' }
      it ('props passed should also be passed up to super', () => {
        const spy = sinon.spy(React.Component.prototype, 'constructor')
        const spyMockDropdown = new Dropdown(props)
        React.Component.prototype.constructor.restore()
        expect (spy.called).to.be.true
        expect (spy.calledWith(props)).to.be.true
      })
      it ('initializes instance variable `state`', () => {
        mockDropdown = new Dropdown(props)
        expect (mockDropdown.state.open).to.be.false
        expect (mockDropdown.state.pattern).to.eq('')
      })
    })
  })
  describe ('.defaultProps', () => {
    it ('exists', () => {
      expect (Dropdown.defaultProps).to.exist
    })
    it ('has correct properties', () => {
      expect (Dropdown.defaultProps).to.have.all.keys('style', 'searchable', 'onSearch')
    })
  })
  describe ('#filterMenu()', () => {
    const mockDropdown = new Dropdown()
    it ('exists with correct number of parameters required', () => {
      expect (mockDropdown.filterMenu).to.exist.to.have.lengthOf(2)
    })
    context ('when given arguments', () => {
      const mockHash = [{value: 'apple'}, {value: 'pear'}, {value: 'plum'}]
      //any issues with these two tests, you might need to research findMatches method as well which is not exported but is a helper method.
      it ('returns correct object for string 4 or greater', () => {
        expect (mockDropdown.filterMenu(mockHash, 'appl')).to.deep.equal([{ value: 'apple', filtered: true}])
      })
      it ('returns original object if less than 4 characters', () => {
        expect (mockDropdown.filterMenu(mockHash, '')).to.eq(mockHash)
      })
    })
  })
  describe ('#handleEvent()', () => {
    const event = { type: 'keyup', keyCode: 27 }
    it ('exists with correct number of parameters required', () => {
      expect (mockDropdown.handleEvent).to.exist.and.have.lengthOf(1)
    })
    context ('when given an event keyCode is 27 and type keyup as an argument', () => {
      it ('triggers close method', () => {
        const spy = sinon.spy(mockDropdown, 'close')
        mockDropdown.handleEvent(event)
        mockDropdown.close.restore()
        expect (spy.calledOnce).to.be.true
      })
    })
    context ('when given any even other than keyCode 27 and type keyup', () => {
      it ('does nothing', () => {
        const diffEvent = { type: 'keydown', keyCode: 28 }
        const spy = sinon.spy(mockDropdown, 'close')
        mockDropdown.handleEvent(diffEvent)
        mockDropdown.close.restore()
        expect (spy.called).to.not.be.true
      })
    })
  })
  describe ('#_toggleMenu()', () => {
    it ('exists with 1 parameter', () => {
      expect (mockDropdown._toggleMenu).to.exist.have.lengthOf(1)
    })
    context ('when passed an event', () => {
      it ('stops event', () => {
        const spy = { preventDefault: sinon.spy() }
        mockDropdown._toggleMenu(spy)
        expect (spy.preventDefault.called).to.be.true
      })
      it ('sets state property of `open` to opposite of it\'s current value once, and with proper key/value', () => {
        const event = { preventDefault: () => {} }
        const spy = sinon.spy(Dropdown.prototype, 'setState')
        const open = mockDropdown.state.open
        mockDropdown._toggleMenu(event)
        Dropdown.prototype.setState.restore()
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith({ open: !open })).to.be.true
      })
    })
  })
  describe ('#close()', () => {
    it ('exists', () => {
      expect (mockDropdown.close).to.exist
    })
    it ('if called, it setState of `open` to false', () => {
        const event = { preventDefault: () => {} }
        const spy = sinon.spy(Dropdown.prototype, 'setState')
        const spyMockDropdown = new Dropdown()
        spyMockDropdown.close(event)
        Dropdown.prototype.setState.restore()
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith({ open: false })).to.be.true
    })
  })
})