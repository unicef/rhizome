import { expect } from 'chai'

import LocationDropdown from '../menus/LocationDropdown'

describe(__filename, () => {
  context('build up location data', () => {
    it('should return data with valid filter', () => {
      const original_locations = [
        {
          'name': 'America - Maine',
          'id': 10,
          'parent_location_id': 1
        }, {
          'name': 'America - Texas',
          'id': 11,
          'parent_location_id': 1
        }, {
          'name': 'England - Merseyside',
          'id': 20,
          'parent_location_id': 2
        }
      ]
      const filter = 'America'
      let location = LocationDropdown.prototype._buildLocations(original_locations, filter)
      expect(location).to.deep.eql([
        {
          'title': 'America - Maine',
          'value': 10,
          'parent': 1
        }, {
          'title': 'America - Texas',
          'value': 11,
          'parent': 1
        }
      ])
    })

    it('should return data without filter or parent location', () => {
      const original_locations = [
        {
          'name': 'America - Maine',
          'id': 10,
          'parent_location_id': 1
        }, {
          'name': 'America - Texas',
          'id': 11,
          'parent_location_id': 1
        }
      ]
      const filter = 'am'
      let location = LocationDropdown.prototype._buildLocations(original_locations, filter)
      expect(location).to.deep.eql([
        {
          'title': 'America - Maine',
          'value': 10,
          'parent': 1
        }, {
          'title': 'America - Texas',
          'value': 11,
          'parent': 1
        }
      ])
    })

    it('should return data without filter but with parent location', () => {
      const original_locations = [
        {
          'name': 'America - Maine',
          'id': 10,
          'parent_location_id': 1
        }, {
          'name': 'America - Texas',
          'id': 11,
          'parent_location_id': 1
        }, {
          'name': 'America',
          'id': 1,
          'parent_location_id': 0
        }
      ]
      const filter = 'am'
      let location = LocationDropdown.prototype._buildLocations(original_locations, filter)
      expect(location).to.deep.eql([
        {
          'children': [
            {
              'title': 'America - Maine',
              'value': 10,
              'parent': 1
            }, {
              'title': 'America - Texas',
              'value': 11,
              'parent': 1
            }
          ],
          'title': 'America',
          'value': 1,
          'parent': 0
        }
      ])
    })

    it('should return data without filter but with parent location, a complex example', () => {
      const original_locations = [
        {
          'name': 'America - Maine',
          'id': 10,
          'parent_location_id': 1
        }, {
          'name': 'America - Texas',
          'id': 11,
          'parent_location_id': 1
        }, {
          'name': 'England - Merseyside',
          'id': 20,
          'parent_location_id': 2
        }, {
          'name': 'America',
          'id': 1,
          'parent_location_id': 0
        }, {
          'name': 'England',
          'id': 2,
          'parent_location_id': 0
        }
      ]
      const filter = 'am'
      let location = LocationDropdown.prototype._buildLocations(original_locations, filter)
      expect(location).to.deep.eql([
        {
          'children': [
            {
              'title': 'America - Maine',
              'value': 10,
              'parent': 1
            }, {
              'title': 'America - Texas',
              'value': 11,
              'parent': 1
            }
          ],
          'title': 'America',
          'value': 1,
          'parent': 0
        }, {
          'children': [
            {
              'title': 'England - Merseyside',
              'value': 20,
              'parent': 2
            }
          ],
          'title': 'England',
          'value': 2,
          'parent': 0
        }
      ])
    })
  })
})
