import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import DropdownButton from '../../button/DropdownButton'
import Dropdown from '../../dropdown/Dropdown'
import sinon from 'sinon'

class DropdownButtonTest {
  static getProps() {
    return {
      text: 'foo',
      items: [{id: 1, title: 'foobar', value: '1'},
              {id: 2, title: 'f00b@r', value: '2'},
              {id: 3, title: 'f()()bar', value: '3'}],
      grouped: true,
      uniqueOnly: false,
      style: '',
      item_plural_name: 'foos'
    }
  }
  static getDefaultProps() {
    return {
      uniqueOnly: false,
      multi: false,
      grouped: false,
      value_field: 'value',
      title_field: 'title',
      icon: 'plus'
    }
  }
  static _toggleMenu() {

  }
  static getComponent() {
    const props = this.getProps()
    if (!props.items || props.items.length === 0) {
      if (props.text) {
        return (
          <button className={props.style} role='button'>
            <i className='fa fa-spinner fa-spin'></i> &nbsp;
            Loading {_.capitalize(props.item_plural_name)}...
          </button>
        )
      } else {
        return <i className='fa fa-spinner fa-spin right'></i>
      }
    }

    const icon = props.icon ? (<i className={['fa', props.icon].join(' ')} />) : null

    return (
        <button className={props.style} role='button' onClick={this._toggleMenu}>
          {icon} {props.text}
        </button>
    )
  }
}

describe ('DropdownButton', () => {
  let mockDropdownButton
  beforeEach (() => {
    mockDropdownButton = new DropdownButton()
  })
  it ('exists', () => {
    expect (DropdownButton).to.exist
  })
  it ('extends Dropdown', () => {
    expect (DropdownButton.prototype instanceof Dropdown).to.be.true
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
        DropdownButton.prototype.setState.restore()
        expect (spy.calledOnce).to.be.true
      })
    })
  })
  describe ('#componentWillUpdate()', () => {
    const props = DropdownButtonTest.getProps()
    it ('exists with 2 arguments', () => {
      expect (mockDropdownButton.componentWillUpdate).to.exist.and.have.lengthOf(2)
    })
    context.skip ('when given 2 arguments and props.grouped is true', () => {
      it ('calls #_getGroupedMenuItemComponents()', () => {
        let props = DropdownButtonTest.getProps()
        props.grouped = true
        const spyMockDropdownButton = new DropdownButton(props)
        const spy = sinon.spy(spyMockDropdownButton, '_getGroupedMenuItemComponents')
        spyMockDropdownButton.componentWillUpdate(props)
        spyMockDropdownButton._getGroupedMenuItemComponents.restore()
        expect (spy.calledOnce).to.be.true
      })
    })
    context.skip ('when given 2 arguments and props.grouped is false', () => {
      it ('calls #_getMenuItemComponents()', () => {
        let props = DropdownButtonTest.getProps()
        props.grouped = false
        const spyMockDropdownButton = new DropdownButton(props)
        const spy = sinon.spy(spyMockDropdownButton, '_getGroupedMenuItemComponents')
        spyMockDropdownButton.componentWillUpdate(props)
        spyMockDropdownButton._getMenuItemComponents.restore()
        expect (spy.calledOnce).to.be.true
      })
    })
    context.skip ('when given 2 arguments', () => {
      it ('calls #_setPattern()', () => {
        const spyMockDropdownButton = new DropdownButton(props)
        const spy = sinon.spy(spyMockDropdownButton, '_setPattern')
        spyMockDropdownButton.componentWillUpdate(props)
        spyMockDropdownButton._setPattern.restore()
        expect (spy.calledOnce).to.be.true
      })
    })
  })
  describe ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<DropdownButton {...DropdownButtonTest.getProps()}/>)
      expectedComponent = DropdownButtonTest.getComponent()
    })
    it ('renders proper jsx', () => {
      const props = DropdownButtonTest.getProps()
      const actualComponent = shallow(<DropdownButton {...props}/>).debug()
      const expectedComponent = shallow(DropdownButtonTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    describe.skip ('events', () => {
      context ('if props has `items`', () => {
        it ('simulates click event', () => {
          let spyMockDropdownButton = new DropdownButton()
          let spy = sinon.spy(spyMockDropdownButton, '_toggleMenu')
          wrapper.find('button').simulate('click',{ preventDefault: () => {} })
          wrapper._toggleMenu.restore()
          expect (spy.calledOnce).to.be.true
        })
      })
      context ('if props has no `items`', () => {
        it ('does NOT simulate click event', () => {
          let spy = sinon.spy(DropdownButton.prototype, '_toggleMenu')
          let props = DropdownButtonTest.getProps()
          props.items = null
          wrapper = shallow(<DropdownButton {...props} />)
          wrapper.find('button').simulate('click')
          DropdownButton.prototype._toggleMenu.restore()
          expect (spy.called).to.be.false
        })
      })
    })
  })
})