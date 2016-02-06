import _ from 'lodash'

var SearchableMenu = {
  getInitialState: function () {
    return {
      pattern: ''
    }
  },

  _setPattern: function (value) {
    this.setState({ pattern: value })
  },

  filterMenu: function (items, pattern) {
    if (_.size(pattern) < 3) return items

    var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'), this)

    return _(items).map(match).flatten().value()
  }
}

function findMatches (item, re) {
  var matches = []
  if (re.test(_.get(item, 'value')) && item.noValue !== true) {
    matches.push(_.assign({}, item, {filtered: true}))
  }
  if (re.test(_.get(item, 'title')) && item.noValue !== true) {
    matches.push(_.assign({}, item, {filtered: true}))
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

export default SearchableMenu
