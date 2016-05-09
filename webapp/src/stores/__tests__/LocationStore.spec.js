import { expect } from 'chai'
import { getMockResponse } from '../../utilities/test/mockData'
import LocationStore from '../LocationStore'

describe (__filename,()=>{
  it ('exists.', () => {
    expect (LocationStore).to.exist
  })
  describe ('#location', () => {
    it ('exists', () => {
      expect (LocationStore.locations).to.exist
    })
    it ('initializes with proper default values', () => {
      const locations = getEmptyLocations()
      expect (LocationStore.locations).to.deep.equal(locations)
    })
  })
  describe ('#getInitialState()', () => {
    it ('exists', () => {
      expect (LocationStore.getInitialState).to.exist
    })
    it ('returns locations property of class', () => {
      const locations = getEmptyLocations()
      expect (LocationStore.getInitialState()).to.deep.equal(locations)
    })
  })
  describe ('#onFetchLocations()',() => {
    it ('exists', () => {
      expect (LocationStore.onFetchLocations).to.exist
    })
    it ('modifies the state\'s \'raw\' property', () => {
      expect (() => { LocationStore.onFetchLocations() }).to.change(LocationStore.state, 'raw')
    })
    it ('sets state of \'raw\' to empty array', () => {
      LocationStore.onFetchLocations()
      expect (LocationStore.state.raw).to.be.empty
    })
  })
  describe ('#onFetchLocationsCompleted()', () => {
    it ('exists', () => {
      expect (LocationStore.onFetchLocationsCompleted).to.exist
    })
    context ('when passed a response parameter', () => {
      const response = getMockResponse()
      it ('updates meta property of state', () => {
        expect(() => { LocationStore.onFetchLocationsCompleted(response) }).to.change(LocationStore.state, 'meta')
      })
      it.skip ('updates raw property of state', () => {
        expect(() => { LocationStore.onFetchLocationsCompleted(response) }).to.change(LocationStore.state, 'raw')
      })
      it ('updates index property of state', () => {
        expect(() => { LocationStore.onFetchLocationsCompleted(response) }).to.change(LocationStore.state, 'index')
      })
      it ('updates list property of state', () => {
        expect(() => { LocationStore.onFetchLocationsCompleted(response) }).to.change(LocationStore.state, 'list')
      })
      it ('updates filtered property of state', () => {
        expect(() => { LocationStore.onFetchLocationsCompleted(response) }).to.change(LocationStore.state, 'filtered')
      })
    })
  })
  describe ('#setLocationLpdStatuses()', () => {
    it ('exists', () => {

    })
  })
})

function getEmptyLocations () {
  return {
          meta: null,
          raw: null,
          index: null,
          filtered: [],
          list: [],
          lpd_statuses: [
            {value: 'lpd-1', 'title': 'LPD 1', location_ids: []},
            {value: 'lpd-2', 'title': 'LPD 2', location_ids: []},
            {value: 'lpd-3', 'title': 'LPD 3', location_ids: []}
          ]
        }
}