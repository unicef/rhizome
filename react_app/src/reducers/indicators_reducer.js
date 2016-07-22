import _ from 'lodash'
import { handleActions } from 'redux-actions'
import treeify from 'utilities/transform/treeify'

const initial_state = {raw: null, index: null, tag_index: null}

export const indicators = handleActions({
  GET_ALL_INDICATORS_SUCCESS: (state, action) => ({
    raw: action.payload.indicators,
    index: _.keyBy(action.payload.indicators, 'id'),
    tree: buildIndicatorsTree(action.payload.indicators, action.payload.indicator_tags, true, true),
    tag_index: processIndicatorsToTags(action.payload.indicator_tags, action.payload.indicators_to_tags)
  })
}, initial_state)

export const indicator = handleActions({
  UPDATE_INDICATOR_SUCCESS: (state, action) => {
    return Object.assign({}, state, action.payload)
  }
}, {
  id: null,
  bad_bound: 0,
  good_bound: 1,
  bound_json: '[]',
  data_format: 'int',
  description: '',
  is_reported: false,
  name: '',
  office_id: '[]',
  resource_name: '',
  short_name: '',
  source_name: '',
  tag_json: '[]'
})

const processIndicatorsToTags = (indicator_tags, indicators_to_tags) => {
  const grouped_by_tag = _.groupBy(indicators_to_tags, 'indicator_tag_id')
  indicator_tags.forEach(tag => {
    tag.indicator_ids = _.map(grouped_by_tag[tag.id], 'indicator_id')
  })
  return _.keyBy(indicator_tags, 'id')
}

// =========================================================================== //
//                                   UTILITIES                                 //
// =========================================================================== //
const makeTagId = (tId) => {
  return 'tag-' + tId
}

const pickAllNodesInTrees = (parent, nodes) => {
  let children = parent.children
  if (children && children.length) {
    children.forEach(item => pickAllNodesInTrees(item, nodes))
  } else {
    if (parent.noValue) nodes.push(parent)
  }
}

const removeIndicatorEmptyNode = (sourceList) => {
  if (!sourceList || !sourceList.length) {
    return sourceList
  }

  let virtualRoot = {noValue: false, parentNode: null, title: 'No Available Indicator', children: sourceList}
  virtualRoot.children.forEach(item => item.parentNode = virtualRoot)

  let nodes
  do {
    nodes = []
    pickAllNodesInTrees(virtualRoot, nodes)
    nodes.forEach(item => item.parentNode.children.splice(item.parentNode.children.indexOf(item), 1))
  } while (nodes.length > 0)

  if (sourceList.length > 0) {
    return sourceList
  } else {
    virtualRoot.noValue = true
    virtualRoot.children = []
    return [virtualRoot]
  }
}

const buildIndicatorsTree = (indicators, tags, isClone, isRemoveEmpty, indicatorFilterType) => {
  if (isClone) {
    tags = _.cloneDeep(tags)
    indicators = _.cloneDeep(indicators)
  }

  let sortTags = _.sortBy(tags, 'tag_name').reverse()

  let tags_map = {}
  sortTags.forEach(tag => {
    tags_map[tag.id] = tag
    tag.id = makeTagId(tag.id)
    tag.noValue = true
    tag.parent = tag.parent_tag_id && tag.parent_tag_id !== 'None' ? makeTagId(tag.parent_tag_id) : null
    tag.children = []
    tag.title = tag.tag_name
    tag.value = tag.id
  })

  // add 'Other Indicators' tag to collect any indicators without tags
  const otherTag = {
    'id': 0,
    'value': makeTagId(0),
    'noValue': true,
    'title': 'Other Indicators',
    'children': []
  }

  indicators.forEach(indicator => {
    indicator.title = indicator.name
    indicator.value = indicator.id
    indicator.displayTitle = indicator.name + ' (' + indicator.id + ')'
    indicator.parsed_tag_json = JSON.parse(indicator.tag_json)

    if (indicatorFilterType) {
      if (!_.isArray(indicator.tag_json) || indicator.tag_json.length === 0) {
        if (indicatorFilterType && indicator.data_format === indicatorFilterType) {
          otherTag.children.push(indicator)
          indicator.parentNode = otherTag
        }
      } else if (_.isArray(indicator.parsed_tag_json)) {
        indicator.parsed_tag_json.forEach(tId => {
          if (indicatorFilterType && indicator.data_format === indicatorFilterType) {
            let tagParent = tags_map[tId]
            tagParent.children.push(indicator)
            indicator.parentNode = tagParent
          }
        })
      }
    } else {
      if (!_.isArray(indicator.parsed_tag_json) || indicator.parsed_tag_json.length === 0) {
        otherTag.children.push(indicator)
        indicator.parentNode = otherTag
      } else if (_.isArray(indicator.parsed_tag_json)) {
        indicator.parsed_tag_json.forEach(tId => {
          let tagParent = tags_map[tId]
          tagParent.children.push(indicator)
          indicator.parentNode = tagParent
        })
      }
    }
  })

  // add other tag?
  if (otherTag.children.length > 0) {
    sortTags.push(otherTag)
  }

  // sort indicators with each tag
  sortTags.forEach(tag => tag.children = _.sortBy(tag.children, 'title'))
  sortTags = treeify(sortTags, 'id')
  sortTags.reverse()

  if (isRemoveEmpty) {
    sortTags = removeIndicatorEmptyNode(sortTags)
  }

  return _.sortBy(sortTags, 'title')
}

