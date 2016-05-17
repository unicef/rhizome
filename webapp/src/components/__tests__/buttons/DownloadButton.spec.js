import React from 'react'
import { Component } from 'react'
import _ from 'lodash'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import DownloadButton from '../../button/DownloadButton'
import sinon from 'sinon'

describe ('DownloadButton', () => {
  let mockDownloadButton
  beforeEach (() => {
    mockDownloadButton = new DownloadButton(DownloadButtonTest.getProps())
  })
  it ('exists', () => {
    expect (DownloadButton).to.exist
  })
  describe ('.propTypes', () => {
    it ('is static and exists', () => {
      expect (DownloadButton.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (DownloadButton.propTypes).to.have.all.keys('data', 'working', 'enable', 'text', 'cookieName', 'onClick', 'classes')
    })
  })
  describe ('#defaults', () => {
    it ('exists', () => {
      expect (mockDownloadButton.defaults).to.exist
    })
    it ('has specified properties', () => {
      expect (mockDownloadButton.defaults).to.have.all.keys('url', 'isWorking')
    })
    it ('has correct initial values', () => {
      const state = DownloadButtonTest.getState()
      expect (mockDownloadButton.defaults.isWorking).to.eq(state.isWorking)
      expect (mockDownloadButton.defaults.url).to.eq(state.url)
    })
  })
  describe ('#getInitialState()', () => {
    it ('exists', () => {
      expect (mockDownloadButton.getInitialState).to.exist
    })
    it ('returns defaults', () => {
      const mockDownloadButton = new DownloadButton()
      expect (mockDownloadButton.getInitialState()).to.deep.eq(mockDownloadButton.defaults)
    })
  })
  describe ('#_completeDownload()', () => {
    it ('exists and has a parameter length of 1', () => {
      expect (mockDownloadButton._completeDownload).to.exist.and.have.lengthOf(1)
    })
    it ('sets state of `isWorking` and `url` to proper values', () => {
      const spyMockDownloadButton = new DownloadButton({ cookieName: '0'})
      const spy = sinon.spy(spyMockDownloadButton, 'setState')
      spyMockDownloadButton._completeDownload(0)
      expect (spy.calledOnce).to.be.true
      spyMockDownloadButton.setState.restore()
    })
    it ('document.cookie is set to proper value', () => {
      const spyMockDownloadButton = new DownloadButton({ cookieName: '0'})
      spyMockDownloadButton._completeDownload(0)
      expect (document._cookie).to.eq('0=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;')
    })
    it ('calls clearInterval with proper arg', () => {
      const spyMockDownloadButton = new DownloadButton({ cookieName: '0'})
      const spy = sinon.spy(window, 'clearInterval')
      spyMockDownloadButton._completeDownload(0)
      expect (spy.called).to.be.true
      expect (spy.calledWith(0)).to.be.true
      window.clearInterval.restore()
    })
  })
  describe ('#_download()', () => {
    let setStateSpy, windowSetIntervalSpy, _completeDownloadSpy, onClickSpy
    beforeEach (() => {
      setStateSpy = sinon.spy(mockDownloadButton, 'setState')
      windowSetIntervalSpy = sinon.spy(window, 'setInterval')
      _completeDownloadSpy = sinon.spy(mockDownloadButton, '_completeDownload')
      onClickSpy = sinon.spy(mockDownloadButton.props, 'onClick')
    })
    afterEach (() => {
      mockDownloadButton.setState.restore()
      window.setInterval.restore()
      mockDownloadButton._completeDownload.restore()
      mockDownloadButton.props.onClick.restore()
    })
    context ('if not enabled or isWorking', () => {
      it ('returns as guard case if `isWorking`', () => {
        const spyMockDownloadButton = new DownloadButton({ isWorking: true})
        setStateSpy = sinon.spy(spyMockDownloadButton, 'setState')
        _completeDownloadSpy = sinon.spy(spyMockDownloadButton, '_completeDownload')
        expect (setStateSpy.called).to.be.false
        expect (windowSetIntervalSpy.called).to.be.false
        expect (_completeDownloadSpy.called).to.be.false
        expect (onClickSpy.called).to.be.false
      })
      it ('returns as guard case if not `enabled`', () => {
        const spyMockDownloadButton = new DownloadButton({ enable: false})
        setStateSpy = sinon.spy(spyMockDownloadButton, 'setState')
        _completeDownloadSpy = sinon.spy(spyMockDownloadButton, '_completeDownload')
        expect (setStateSpy.called).to.be.false
        expect (windowSetIntervalSpy.called).to.be.false
        expect (_completeDownloadSpy.called).to.be.false
        expect (onClickSpy.called).to.be.false
      })
    })
    context ('if enabled or not isWorking', () => {
      it ('sets state for `url` and `isWorking`', () => {
        mockDownloadButton._download()
        expect (setStateSpy.calledOnce).to.be.true
        expect (setStateSpy.calledWith({ url: DownloadButtonTest.getProps().onClick(), isWorking: true })).to.be.true
      })
      it ('calls window.setInterval', () => {
        mockDownloadButton._download()
        expect (windowSetIntervalSpy.calledOnce).to.be.true
        //this appears to not validate even when I force a false positive. need to research this perhaps a deep
        //equals is required
        // expect (windowSetIntervalSpy.calledWith(windowSetIntervalSpy.args[0], windowSetIntervalSpy.args[1])).to.be.true
      })
      it.skip ('calls #_completeDownload()', () => {
        //need to research into hooking into asyncrhonous calls with window
        mockDownloadButton._download()
        expect (_completeDownloadSpy.calledOnce).to.be.true
        // expect (_completeDownloadSpy.calledWith(0)).to.be.true
      })
    })
  })
  describe.skip ('#_getCookie()', () => {
    //currently being skipped because this method is not being used
    context ('if cookie length is greater than 0', () => {
      it ('returns cookie', () => {

      })
    })
    context ('if cookie length is greater than 0', () => {
      it ('returns empty string', () => {

      })
    })
  })
  describe ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<DownloadButton {...DownloadButtonTest.getProps()}/>)
      expectedComponent = DownloadButtonTest.mockComponent()
    })
    it.skip ('renders correct components', () => {
      expect (wrapper.equals(expectedComponent)).to.be.true
    })
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    it.skip ('contains an inner component', () => {
      expect (wrapper.contains(DownloadButtonTest.mockInnerComponent())).to.be.true
    })
    describe ('events', () => {
      it ('simulates click events', () => {
        let spy = sinon.spy(DownloadButton.prototype.__reactAutoBindMap, "_download")
        wrapper = shallow(<DownloadButton {...DownloadButtonTest.getProps()} />)
        wrapper.find('button').simulate('click')
        expect (spy.calledOnce).to.be.true
        DownloadButton.prototype.__reactAutoBindMap._download.restore()
      })
    })
  })
})
class DownloadButtonTest {
  static getProps() {
    //update working variable if isWorking is switched to true
    return {
      text: 'stuff',
      enable: true,
      classes: '',
      working: 'bar',
      cookieName: 'foo',
      onClick: () => 'empty'
    }
  }
  static getRefreshIntervalArgs() {
    return [ () => {
      // var cookieValue = self._getCookie(self.props.cookieName)
      // if (cookieValue === 'true') {
      _this._completeDownload(refreshIntervalId);
      // }
    }, 1000]
  }
  static getState() {
    return {
      isWorking: false,
      url: 'about:blank'
    }
  }
  static _download () {

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