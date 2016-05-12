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
    it ('is exists', () => {
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
      expectedComponent = IconButtonTest.mockComponent()
    })
    it.skip ('renders correct components', () => {
      expect (wrapper.equals(expectedComponent)).to.be.true
    })
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    it.skip ('contains an inner component', () => {
      expect (wrapper.contains(IconButtonTest.mockInnerComponent())).to.be.true
    })
    it.skip ('simulates click events', () => {
      let spy = sinon.spy(IconButton.prototype.__reactAutoBindMap, "_download")
      wrapper = shallow(<IconButton {...IconButtonTest.getProps()} />)
      wrapper.find('button').simulate('click')
      expect (spy.calledOnce).to.be.true
      IconButton.prototype.__reactAutoBindMap._download.restore()
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
      working: 'bar',
      cookieName: 'foo',
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
      isWorking: false,
      url: 'about:blank'
    }
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