import { expect } from 'chai'

import { childOf } from '../dashboardInit.js'

describe(__filename, () => {
  context('child of', () => {
    context('child has no parent', () => {
      it('child has no parent_location_id', () => {
        let child = {
          not_parent: 1
        }
        let parent = {}
        expect(childOf(parent, child)).to.be.false
      })

      it('child has parent_location_id equals to parent.id', () => {
        let child = {
          parent_location_id: 1
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.true
      })
      it('child has parent_location_id not equal to parent.id', () => {
        let child = {
          parent_location_id: 1
        }
        let parent = {
          id: 2
        }
        expect(childOf(parent, child)).to.be.false
      })
    })

    context('child has parent', () => {
      it('child has parent.id equal to parent.id', () => {
        let child = {
          parent: {
            id: 1
          }
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.true
      })
      it('child has parent.id not equal to parent.id, recursively call true case', () => {
        let child = {
          parent: {
            parent: {
              id: 1
            }
          }
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.true
      })
      it('child has parent.id not equal to parent.id, recursively call false case', () => {
        let child = {
          parent: {
            parent: {
              no_parent: 2
            }
          }
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.false
      })
    })
  })
})
