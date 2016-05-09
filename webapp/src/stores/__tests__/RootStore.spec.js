// import { expect } from 'chai'
// import { getEmptyData, getMockResponse, getMockError } from '../../utilities/test/mockData'
// import RootStore from '../RootStore'

// describe (__filename, () => {
//   it ('is able to be imported', () => {
//     expect (RootStore).to.exist
//   })
//   describe ('#listenables', () => {
//     it ('exists', () => {
//       expect (RootStore.listenables).to.exist
//     })
//   })

//   describe ('#mixins', () => {
//     it ('exists', () => {
//       expect (RootStore.mixins).to.exist
//     })
//   })

//   describe ('#data', () => {
//     it ('exists', () => {
//       expect (RootStore.mixins).to.exist
//     })
//     //gets class declaration value, rather than instance
//     const initial_loading_state = RootStore.getInitialState().loading
//     it ('#loading initializes as false', () => {
//       expect (initial_loading_state).to.be.false
//     })
//   })

//   describe ('#onFetchAllMeta()', () => {
//     it ('exists', () => {
//       expect (RootStore).to.respondTo('onFetchAllMeta')
//     })
//   })

//   describe ('#onFetchAllMetaCompleted()', () => {
//     it ('exists', () => {
//       expect (RootStore).to.respondTo('onFetchAllMetaCompleted')
//     })

//     context ('receiving a successful response from get_all_meta API', () => {
//       const mocked_response = getMockResponse()
//       it ('updates state of campaigns', () => {
//         expect (() => { RootStore.onFetchAllMetaCompleted(mocked_response) }).to.change(RootStore.data, 'campaigns')
//       })
//       it ('updates state of indicators', () => {
//         expect (() => { RootStore.onFetchAllMetaCompleted(mocked_response) }).to.change(RootStore.data, 'indicators')
//       })
//       it ('updates state of locations', () => {
//         expect (() => { RootStore.onFetchAllMetaCompleted(mocked_response) }).to.change(RootStore.data, 'locations')
//       })
//       it ('updates state of dashboards', () => {
//         expect (() => { RootStore.onFetchAllMetaCompleted(mocked_response) }).to.change(RootStore.data, 'dashboards')
//       })
//       it ('updates state of offices', () => {
//         expect (() => { RootStore.onFetchAllMetaCompleted(mocked_response) }).to.change(RootStore.data, 'offices')
//       })
//       it ('updates state of charts', () => {
//         expect (() => { RootStore.onFetchAllMetaCompleted(mocked_response) }).to.change(RootStore.data, 'charts')
//       })
//     })
//   })

//   describe ('#onFetchAllMetaFailed()', () => {
//     it ('exists', () => {
//       expect (RootStore).to.respondTo('onFetchAllMetaFailed')
//     })
//     context ('receiving a failed response from get_all_meta API',() => {
//       before(() => {
//         RootStore.data = getEmptyData()
//       })
//       it.skip ('sets state error', () => { // needs to be fixed in code, api throws error
//         const errorResponse = getMockError()
//         expect(() => { RootStore.onFetchAllMetaFailed(errorResponse) }).to.change(RootStore.data, 'error')
//       })
//     })
//   })
// })