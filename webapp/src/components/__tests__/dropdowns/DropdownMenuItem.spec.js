import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import DropdownMenuItem from '../../dropdown/DropdownMenuItem'
import sinon from 'sinon'

describe ('DropdownMenuItem', () => {
  it ('exists', () => {
    expect (DropdownMenuItem).to.exist
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (DropdownMenuItem.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (DropdownMenuItem.propTypes).to.have.all.keys('key', 'text', 'onClick', 'classes')
    })
  })
  describe ('#render()', () => {
    it ('exists', () => {
      const mockDropdownMenuItem = new DropdownMenuItem()
      expect (mockDropdownMenuItem.render).to.exist
    })
    it ('renders correct jsx', () => {
      const props = DropdownMenuItemTest.getProps()
      const actualComponent = shallow(<DropdownMenuItem {...props}/>).debug()
      const expectedComponent = shallow(DropdownMenuItemTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
  })
})

class DropdownMenuItemTest {
  static getProps() {
    return {
      key: 'foo',
      text: 'bar',
      onClick: () => 'nothing',
      classes: ''
    }
  }
  static getComponent() {
    const props = this.getProps()
    return (
      <li key={props.key} className={props.classes}>
        <a role='menuitem' onClick={props.onClick}>
          {props.text}
        </a>
      </li>
    )
  }
}