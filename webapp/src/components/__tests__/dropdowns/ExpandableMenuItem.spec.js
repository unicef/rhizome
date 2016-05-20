import React from 'react'
import _ from 'lodash'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import ExpandableMenuItem from '../../dropdown/ExpandableMenuItem'
import sinon from 'sinon'

describe ('ExpandableMenuItem', () => {
  let mockExpandableMenuItem
  beforeEach (() => {
    mockExpandableMenuItem = shallow(<ExpandableMenuItem />).instance()
  })
  it ('exists', () => {
    expect (ExpandableMenuItem).to.exist
  })
  describe ('.propTypes', () => {
    it ('exists', () => {
      expect (ExpandableMenuItem.propTypes).to.exist
    })
    it ('has the correct keys', () => {
      expect (ExpandableMenuItem.propTypes).to.have.all.keys('sendValue', 'title', 'value', 'classes', 'ancestryString', 'children', 'depth', 'disabled', 'filtered', 'displayTitle', 'noValue', 'hideLastLevel')
    })
  })
  describe ('.fromArray()', () => {
    it ('exists', () => {
      expect (ExpandableMenuItem.fromArray).to.exist
    })
  })
  describe ('.getDefaultProps()', () => {
    it ('exists', () => {
      expect (ExpandableMenuItem.getDefaultProps).to.exist
    })
    it ('returns correct default key and values', () => {
      const defaultProps = ExpandableMenuItem.getDefaultProps()
      const expectedDefaultProps = ExpandableMenuItemTest.getProps()
      expect (defaultProps).to.have.all.keys('depth', 'filtered', 'hideLastLevel', 'displayTitle')
      expect (defaultProps.depth).to.eq(expectedDefaultProps.depth)
      expect (defaultProps.filtered).to.eq(expectedDefaultProps.filtered)
      expect (defaultProps.hideLastLevel).to.eq(expectedDefaultProps.hideLastLevel)
      expect (defaultProps.displayTitle).to.eq(expectedDefaultProps.displayTitle)
    })
  })
  describe ('.getInitialState()', () => {
    it ('exists', () =>{
      expect (mockExpandableMenuItem.getInitialState).to.exist
    })
    it ('returns correct default key and values', () => {
      const defaultState = mockExpandableMenuItem.getInitialState()
      const expectedInitialState = ExpandableMenuItemTest.getState()
      expect (defaultState).to.have.all.keys('open', 'disabled')
      expect (defaultState.open).to.eq(expectedInitialState.open)
      expect (defaultState.disabled).to.eq(expectedInitialState.disabled)
    })
  })
  describe ('#componentDidMount()', () => {
    it ('exists', () => {
      expect (mockExpandableMenuItem.componentDidMount).to.exist
    })
    it ('sets state for `disabled`', () => {
      const prototype = ExpandableMenuItem.prototype
      const spy = sinon.spy(prototype, 'setState')
      const wrapper = shallow(<ExpandableMenuItem {...ExpandableMenuItemTest.getProps()}/>)
      wrapper.instance().componentDidMount()
      prototype.setState.restore()
      expect (wrapper.instance().state.disabled).to.eq(ExpandableMenuItemTest.getProps().disabled)
      expect (spy.calledOnce).to.be.true
      expect (spy.calledWith({disabled: ExpandableMenuItemTest.getProps().disabled})).to.be.true
    })
  })
  describe ('#componentWillUpdate()', () => {
    it ('exists with correct parameters', () => {
      expect (mockExpandableMenuItem.componentWillUpdate).to.exist.and.have.lengthOf(2)
    })
    context ('when props.disabled not equal to nextProps.disabled', () => {
      it ('sets state of `disabled` to nextProps.disabled', () => {
        const prototype = ExpandableMenuItem.prototype
        const spy = sinon.spy(prototype, 'setState')
        const props = ExpandableMenuItemTest.getProps()
        const nextProps = { disabled: !props.disabled }
        const wrapper = shallow(<ExpandableMenuItem {...props}/>)
        wrapper.instance().componentWillUpdate(nextProps)
        prototype.setState.restore()
        expect (wrapper.instance().state.disabled).to.eq(nextProps.disabled)
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith({disabled: nextProps.disabled})).to.be.true
      })
      it ('sets state of `disabled` to nextProps.disabled', () => {
        const prototype = ExpandableMenuItem.prototype
        const spy = sinon.spy(prototype, 'setState')
        const props = ExpandableMenuItemTest.getProps()
        const wrapper = shallow(<ExpandableMenuItem {...props}/>)
        wrapper.instance().componentWillUpdate(props)
        prototype.setState.restore()
        expect (wrapper.instance().state.disabled).to.eq(props.disabled)
        expect (spy.called).to.be.false
      })
    })
  })
  describe ('#_toggleChildren()', () => {
    it ('exists with correct parameters', () => {
      expect (mockExpandableMenuItem._toggleChildren).to.exist.and.have.lengthOf(1)
    })
    it ('calls stopPropagation on event', () => {
      const spy = sinon.spy()
      mockExpandableMenuItem._toggleChildren({type: 'keyup', stopPropagation: spy})
      expect (spy.calledOnce).to.be.true
    })
    it ('sets state `open` to opposite of current state.open', () => {
      const prototype = ExpandableMenuItem.prototype
      const spy = sinon.spy(prototype, 'setState')
      const props = ExpandableMenuItemTest.getProps()
      const wrapper = shallow(<ExpandableMenuItem {...props}/>)
      const state = wrapper.instance().state
      wrapper.instance()._toggleChildren({type: 'keyup', stopPropagation: () => null})
      prototype.setState.restore()
      expect (wrapper.instance().state.open).to.not.eq(state.open)
      expect (spy.calledOnce).to.be.true
      expect (spy.calledWith({open: !state.open})).to.be.true
    })
  })
  describe ('#_handleClick()', () => {
    it ('exists with correct parameters', () => {
      expect (mockExpandableMenuItem._handleClick).to.exist.and.have.lengthOf(1)
    })
    context ('if props.noValue is false and state.disabled is false', () => {
      it ('calls props.sendValue and setState', () => {
        let props = ExpandableMenuItemTest.getProps()
        const sendValueSpy = sinon.spy()
        props.sendValue = sendValueSpy
        props.noValue = false
        const prototype = ExpandableMenuItem.prototype
        const setStateSpy = sinon.spy(prototype, 'setState')
        mockExpandableMenuItem = shallow(<ExpandableMenuItem {...props} />).instance()
        mockExpandableMenuItem._handleClick({type: 'keyup'})
        prototype.setState.restore()
        expect (sendValueSpy.calledOnce).to.be.true
        expect (sendValueSpy.calledWith(props.value)).to.be.true
        expect (setStateSpy.calledOnce).to.be.true
        expect (setStateSpy.calledWith({disabled: true})).to.be.true
      })
    })
    context ('if props.noValue or state.disabled is false', () => {
      const e = {type: 'keyup', stopPropagation: () => null}
      it ('calls #_toggleChildren()', () => {
        let props = ExpandableMenuItemTest.getProps()
        props.noValue = false
        const spy = sinon.spy(ExpandableMenuItem.prototype.__reactAutoBindMap, '_toggleChildren')
        mockExpandableMenuItem = shallow(<ExpandableMenuItem {...props} />).instance()
        mockExpandableMenuItem.state.disabled = true
        mockExpandableMenuItem._handleClick(e)
        const calledOnce = spy.calledOnce
        const calledWith = spy.calledWith(e)
        ExpandableMenuItem.prototype.__reactAutoBindMap._toggleChildren.restore()
        expect (calledOnce).to.be.true
        expect (calledWith).to.be.true
      })
      it ('calls #_toggleChildren()', () => {
        let props = ExpandableMenuItemTest.getProps()
        props.noValue = true
        const spy = sinon.spy(ExpandableMenuItem.prototype.__reactAutoBindMap, '_toggleChildren')
        mockExpandableMenuItem = shallow(<ExpandableMenuItem {...props} />).instance()
        mockExpandableMenuItem.state.disabled = false
        mockExpandableMenuItem._handleClick(e)
        ExpandableMenuItem.prototype.__reactAutoBindMap._toggleChildren.restore()
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith(e)).to.be.true
      })
    })
  })
  describe ('#render()', () => {
    it ('exists', () => {
      mockExpandableMenuItem = new ExpandableMenuItem()
      expect (mockExpandableMenuItem.render).to.exist
    })
    it ('renders correct jsx', () => {
      const props = ExpandableMenuItemTest.getProps()
      const actualComponent = shallow(<ExpandableMenuItem {...props}/>).debug()
      const expectedComponent = shallow(ExpandableMenuItemTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
  })
})

class ExpandableMenuItemTest {
  static getProps() {
    return {
      disabled: false,
      depth: 0,
      filtered: false,
      hideLastLevel: false,
      displayTitle: null,
      classes: '',
      onClick: this._handleClick,
    }
  }
  static getState() {
    return {
      open: false,
      disabled: false
    }
  }
  static _handleClick() {
    return null
  }
  static getComponent() {
    const props = this.getProps()
    let state = this.getState()
    const hasChildren = !props.filtered && _.isArray(props.children) && props.children.length > 0
    const isLastParent = props.children && props.children.filter(child => child.children).length < 1
    const hideArrow = isLastParent && props.hideLastLevel
    const prefix = props.filtered ? _.get(props, 'ancestryString', '') : ''
    const title = prefix + (props.displayTitle === null ? props.title : props.displayTitle)

    var children = null
    if (props.children && state.open) {
      children = props.children.map(item => {
        return <MenuItem key={item.value} depth={props.depth + 1} sendValue={props.sendValue} {...item} hideLastLevel={props.hideLastLevel}/>
      })
    }

    var arrowStyle = {
      paddingLeft: state.filtered ? '5px' : (5 + (17 * props.depth)) + 'px',
      display: 'inline-block'
    }
    const arrow_button = hasChildren ? (
      <a onClick={this._toggleChildren} className={hasChildren ? 'folder' : null} style={arrowStyle}>
        <i className={'fa fa-lg fa-fw fa-caret-' + (state.open ? 'down' : 'right')}></i>
      </a>
    ) : null

    let itemStyle = { display: 'inline-block' }
    let classes = state.disabled ? ' disabled ' : ''
    classes += hasChildren ? 'folder' : ''
    !hasChildren || hideArrow ? itemStyle.paddingLeft = state.filtered ? '5px' : (15 + (18 * props.depth)) + 'px' : null
    const item_button = (
      <a role='menuitem' onClick={this._handleClick} style={itemStyle} tabIndex='-1' className={classes} >
        {title}
      </a>
    )
    return (
      <li className={props.classes}>
        { hideArrow ? null : arrow_button }
        { item_button }
        <div>
          {children}
        </div>
      </li>
    )
  }
}