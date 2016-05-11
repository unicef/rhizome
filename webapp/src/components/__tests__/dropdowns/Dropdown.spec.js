import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import Dropdown from '../../dropdown/Dropdown'
import sinon from 'sinon'

describe ('Dropdown', () => {
  it ('exists', () => {
    expect (Dropdown).to.exist
  })
  it ('extends Component class of React', () => {
    const mockDropdown = new Dropdown()
    expect (mockDropdown instanceof React.Component).is.eq(true)
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
    const mockHash = [{value: 'apple'}, {value: 'pear'}, {value: 'plum'}]
    it ('exists with correct number of parameters required', () => {
      expect (mockDropdown.filterMenu).to.exist.to.have.lengthOf(2)
    })
    context ('when given arguments', () => {
      it ('returns correct object for string 4 or greater', () => {
        expect (mockDropdown.filterMenu(mockHash, 'appl')).to.deep.equal([{ value: 'apple', filtered: true}])
      })
      it ('returns original object if less than 4 characters', () => {
        expect (mockDropdown.filterMenu(mockHash, '')).to.eq(mockHash)
      })
    })
  })
  describe ('#handleEvent()', () => {
    const mockDropdown = new Dropdown()
    const event = { type: 'keyup', keyCode: 27 }
    it ('exists with correct number of parameters required', () => {
      expect (mockDropdown.handleEvent).to.exist.and.have.lengthOf(1)
    })
    context ('when given an event keyCode is 27 and type keyup as an argument', () => {
      it.skip ('triggers close method', () => {
        //not recognizing method
        const spy = sinon.spy(Dropdown.prototype.__reactAutoBindMap, 'close')
        const spyMockDropdown = new Dropdown()
        spyMockDropdown.handleEvent(event)
        expect (spy.calledOnce).to.eq(true)
        spy.restore()
      })
    })
  })
})