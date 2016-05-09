import _ from 'lodash'
import chai from 'chai'
import { should } from 'chai'
import { expect } from 'chai'
// import spies from 'chai-spies'
import { getMockResponse } from '../../utilities/test/mockData'
import IndicatorStore from '../IndicatorStore'

// chai.use(spies)

describe (__filename, () => {
  it ('exists', () => {
    expect (IndicatorStore).to.exist
  })
  describe ('#indicators', () => {
    it ('exists', () => {
      expect (IndicatorStore.indicators).to.exist
    })
    it ('has proper default values', () => {
      expect (IndicatorStore.indicators).to.deep.equal(IndicatorStore.getInitialState())
    })
  })
  describe ('#onFetchIndicators()', () => {
    it ('exists', () => {
      expect (IndicatorStore.onFetchIndicators).to.exist
    })
    it ('changes state for raw', () => {
      expect (() => IndicatorStore.onFetchIndicators()).to.change(IndicatorStore.state, 'raw')
    })
  })
  describe ('#onFetchIndicatorsCompleted()', () => {
    it ('exists', () => {
      expect (IndicatorStore).to.exist
    })
    context ('when given response argument', () => {
      it ('updates meta property', () => {
        let response = getMockResponse()
        response.meta = 'stuff'
        expect (() => IndicatorStore.onFetchIndicatorsCompleted(response)).to.change(IndicatorStore.state, 'meta')
      })
      it ('updates raw property', () => {
        const response = getMockResponse()
        expect (() => IndicatorStore.onFetchIndicatorsCompleted(response)).to.change(IndicatorStore.state, 'raw')
      })
      it ('updates filtered property', () => {
        const response = getMockResponse()
        expect (() => IndicatorStore.onFetchIndicatorsCompleted(response)).to.change(IndicatorStore.state, 'filtered')
      })
      it ('updates index property', () => {
        const response = getMockResponse()
        expect (() => IndicatorStore.onFetchIndicatorsCompleted(response)).to.change(IndicatorStore.state, 'index')
      })
    })
    it.skip ('calls #processIndicators() once', () => {
      // const spy = chai.spy(IndicatorStore.processIndicators)
      const response = getMockResponse()
      IndicatorStore.onFetchIndicatorsCompleted(response)
      // expect(spy).to.have.been.called()
    })
  })
})

function clearStore () {
  IndicatorStore.state = {
                          meta: null,
                          raw: null,
                          index: null,
                          filtered: [],
                          list: [],
                          tree: []
                        }
}