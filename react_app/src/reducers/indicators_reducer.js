import _ from 'lodash'
import { handleActions } from 'redux-actions'

const initial_state = {raw: null, index: null, tag_index: null}

const indicators = handleActions({
  GET_ALL_INDICATORS_SUCCESS: (state, action) => ({
    raw: action.payload.indicators,
    index: _.keyBy(action.payload.indicators, 'id'),
    tag_index: processIndicatorsToTags(action.payload.indicator_tags, action.payload.indicators_to_tags)
  })
}, initial_state)

const processIndicatorsToTags = (indicator_tags, indicators_to_tags) => {
  const grouped_by_tag = _.groupBy(indicators_to_tags, 'indicator_tag_id')
  indicator_tags.forEach(tag => {
    tag.indicator_ids = _.map(grouped_by_tag[tag.id], 'indicator_id')
  })
  return _.keyBy(indicator_tags, 'id')
}

export default indicators
