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
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (DropdownMenu.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (DropdownMenu.propTypes).to.have.all.keys('icon', 'color', 'alt_text', 'text', 'className', 'onClick', 'style', 'isBusy')
    })
  })
  describe ('#getDefaultProps()', () => {
    it ('exists', () => {
      expect (DropdownMenu.getDefaultProps).to.exist
    })
    it ('returns specified properties', () => {
      expect (DropdownMenu.getDefaultProps()).to.have.all.keys('color', 'icon', 'text', 'alt_text', 'isBusy', 'style')
    })
    it ('has correct initial values', () => {
      const expectedProps = DropdownMenuTest.getDefaultProps()
      const actualProps = DropdownMenu.getDefaultProps()
      expect (actualProps.color).to.eq(expectedProps.color)
      expect (actualProps.icon).to.eq(expectedProps.icon)
      expect (actualProps.text).to.eq(expectedProps.text)
      expect (actualProps.alt_text).to.eq(expectedProps.alt_text)
      expect (actualProps.isBusy).to.eq(expectedProps.isBusy)
      expect (actualProps.style).to.deep.eq(expectedProps.style)
    })
  })
  describe ('#getInitialState()', () => {
    it ('exists', () => {
      expect (mockDropdownMenu.getInitialState).to.exist
    })
    it ('returns defaults', () => {
      expect (mockDropdownMenu.getInitialState()).to.deep.eq({ tooltip: null })
    })
  })
  describe ('#showTooltip()', () => {
    it ('exists', () => {
      expect (mockDropdownMenu.showTooltip).to.exist.and.have.lengthOf(1)
    })
    context ('when an event argument is given', () => {
      const event = { pageX: 10, pageY: 11 }
      context ('and the props text is undefined or null', () => {
        it ('returns nothing', () => {
          expect (mockDropdownMenu.showTooltip(event)).to.not.exist
        })
      })
      context ('and the props text has a value', () => {
        it.skip ('sets state of `tooltip` as a tooltip component', () => {
          const text = { text: 'foo' }
          const mockIconButtonWithText = new DropdownMenu({ text })
          const wrapper = shallow(<DropdownMenu text='foo'/>)
          wrapper.instance().showTooltip(event)
          const expectedTooltip = wrapper.instance().state.tooltip
          const actualTooltip = <Tooltip left={event.pageX} top={event.pageY}>{ DropdownMenuTest.getDefaultProps().isBusy ? DropdownMenuTest.getDefaultProps().alt_text : text }</Tooltip>
          expect (expectedTooltip.equals(actualTooltip)).to.be.true
        })
      })
    })
  })
  describe ('#hideTooltip()', () => {
    it ('exists', () => {
      expect (mockDropdownMenu.hideTooltip).to.exist
    })
    it.skip ('destroys state of `tooltip` when called', () => {
      //need to implement document react-layer
      mockDropdownMenu.state.tooltip = shallow(<Tooltip />)
      mockDropdownMenu.hideTooltip()
      expect (mockDropdownMenu.state.tooltip).to.not.exist
    })
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
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    it.skip ('contains an inner component', () => {
      expect (wrapper.contains(DropdownMenuTest.mockInnerComponent())).to.be.true
    })
    it ('simulates click events', () => {
      let spy = sinon.spy()
      wrapper = shallow(<DropdownMenu onClick={spy}/>)
      wrapper.find('button').simulate('click')
      expect (spy.calledOnce).to.be.true
    })
    it ('simulates mouseOver events', () => {
      let reactPrototype = DropdownMenu.prototype.__reactAutoBindMap
      let spy = sinon.spy(reactPrototype, 'showTooltip')
      wrapper = shallow(<DropdownMenu />)
      wrapper.find('button').simulate('mouseover')
      expect (spy.calledOnce).to.be.true
      reactPrototype.showTooltip.restore()
    })
    it ('simulates mouseOut events', () => {
      let reactPrototype = DropdownMenu.prototype.__reactAutoBindMap
      let spy = sinon.spy(reactPrototype, 'hideTooltip')
      wrapper = shallow(<DropdownMenu />)
      wrapper.find('button').simulate('mouseout')
      expect (spy.calledOnce).to.be.true
      reactPrototype.hideTooltip .restore()
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
      tooltip: null,
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
  static mockInnerComponent() {
    const props = this.getProps()
    return (
      <i
        className={'fa ' + (props.isBusy ? 'fa-spinner fa-spin' : props.icon)}
        style={{color: props.color}}
      />
    )
  }
}