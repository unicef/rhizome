import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import IconButton from '../../button/IconButton'
import Tooltip from '../../Tooltip'
import sinon from 'sinon'

describe ('IconButton', () => {
  let mockIconButton
  beforeEach (() => {
    mockIconButton = new IconButton(IconButtonTest.getDefaultProps())
  })
  it ('exists', () => {
    expect (IconButton).to.exist
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (IconButton.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (IconButton.propTypes).to.have.all.keys('icon', 'color', 'alt_text', 'text', 'className', 'onClick', 'style', 'isBusy')
    })
  })
  describe ('#getDefaultProps()', () => {
    it ('exists', () => {
      expect (IconButton.getDefaultProps).to.exist
    })
    it ('returns specified properties', () => {
      expect (IconButton.getDefaultProps()).to.have.all.keys('color', 'icon', 'text', 'alt_text', 'isBusy', 'style')
    })
    it ('has correct initial values', () => {
      const expectedProps = IconButtonTest.getDefaultProps()
      const actualProps = IconButton.getDefaultProps()
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
      expect (mockIconButton.getInitialState).to.exist
    })
    it ('returns defaults', () => {
      expect (mockIconButton.getInitialState()).to.deep.eq({ tooltip: null })
    })
  })
  describe ('#showTooltip()', () => {
    it ('exists', () => {
      expect (mockIconButton.showTooltip).to.exist.and.have.lengthOf(1)
    })
    context ('when an event argument is given', () => {
      const event = { pageX: 10, pageY: 11 }
      context ('and the props text is undefined or null', () => {
        it ('returns nothing', () => {
          expect (mockIconButton.showTooltip(event)).to.not.exist
        })
      })
      context ('and the props text has a value', () => {
        it.skip ('sets state of `tooltip` as a tooltip component', () => {
          const text = { text: 'foo' }
          const mockIconButtonWithText = new IconButton({ text })
          const wrapper = shallow(<IconButton text='foo'/>)
          wrapper.instance().showTooltip(event)
          const expectedTooltip = wrapper.instance().state.tooltip
          const actualTooltip = <Tooltip left={event.pageX} top={event.pageY}>{ IconButtonTest.getDefaultProps().isBusy ? IconButtonTest.getDefaultProps().alt_text : text }</Tooltip>
          expect (expectedTooltip.equals(actualTooltip)).to.be.true
        })
      })
    })
  })
  describe ('#hideTooltip()', () => {
    it ('exists', () => {
      expect (mockIconButton.hideTooltip).to.exist
    })
    it.skip ('destroys state of `tooltip` when called', () => {
      //need to implement document react-layer
      mockIconButton.state.tooltip = shallow(<Tooltip />)
      mockIconButton.hideTooltip()
      expect (mockIconButton.state.tooltip).to.not.exist
    })
  })
  describe ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<IconButton {...IconButtonTest.getProps()}/>)
      expectedComponent = IconButtonTest.getComponent()
    })
    it ('renders proper jsx', () => {
      const props = IconButtonTest.getProps()
      const actualComponent = shallow(<IconButton {...props}/>).debug()
      const expectedComponent = shallow(IconButtonTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    describe ('events', () => {
      it ('simulates click events', () => {
        let spy = sinon.spy()
        wrapper = shallow(<IconButton onClick={spy}/>)
        wrapper.find('button').simulate('click')
        expect (spy.calledOnce).to.be.true
      })
      it ('simulates mouseOver events', () => {
        let reactPrototype = IconButton.prototype.__reactAutoBindMap
        let spy = sinon.spy(reactPrototype, 'showTooltip')
        wrapper = shallow(<IconButton />)
        wrapper.find('button').simulate('mouseover')
        reactPrototype.showTooltip.restore()
        expect (spy.calledOnce).to.be.true
      })
      it ('simulates mouseOut events', () => {
        let reactPrototype = IconButton.prototype.__reactAutoBindMap
        let spy = sinon.spy(reactPrototype, 'hideTooltip')
        wrapper = shallow(<IconButton />)
        wrapper.find('button').simulate('mouseout')
        reactPrototype.hideTooltip .restore()
        expect (spy.calledOnce).to.be.true
      })
    })
  })
})
class IconButtonTest {
  static getProps() {
    //update working variable if isWorking is switched to true
    return {
      text: 'stuff',
      enable: true,
      classes: '',
      className: 'foo',
      working: 'bar',
      cookieName: 'foo',
      icon: 'info-circle',
      onClick: () => {}
    }
  }
  static getDefaultProps() {
    return {
      color: null,
      icon: 'info-circle',
      text: null,
      alt_text: 'Loading ...',
      isBusy: false,
      style: {fontSize: '2rem'}
    }
  }
  static getState() {
    return {
      tooltip: null,
    }
  }
  static showTooltip() {

  }
  static hideTooltip() {

  }
  static getComponent() {
    const props = this.getProps()
    const state = this.getState()
    return (
      <button
        onClick={props.onClick}
        onMouseOver={this.showTooltip}
        onMouseOut={this.hideTooltip}
        className={'button icon-button ' + props.className}>
        {this.getInnerComponent()}
      </button>
    )
  }
  static getInnerComponent() {
    const props = this.getProps()
    return (
      <i
        className={'fa ' + (props.isBusy ? 'fa-spinner fa-spin' : props.icon)}
        style={{color: props.color}}
      />
    )
  }
}