import _ from 'lodash'
import { handleActions } from 'redux-actions'

const data = {raw: null, index: null, tag_index: null}

const indicators = handleActions({
  FETCH_INDICATORS: (state, action) => processIndicators(action.payload.data.objects),
  FETCH_INDICATOR_TAGS: (state, action) => processIndicatorTags(action.payload.data.objects),
  FETCH_INDICATORS_TO_TAGS: (state, action) => processIndicatorsToTags(action.payload.data.objects),
  GET_INITIAL_DATA_SUCCESS: (state, action) => {
    processIndicators(action.payload.data.objects[0].indicators)
    processIndicatorTags(action.payload.data.objects[0].indicator_tags)
    processIndicatorsToTags(action.payload.data.objects[0].indicators_to_tags)
    return data
  }
}, data)

const processIndicators = (indicators) => {
  data.raw = indicators
  data.index = _.keyBy(indicators, 'id')
}

const processIndicatorTags = (indicator_tags) => {
  data.tag_index = _.keyBy(indicator_tags, 'id')
}

const processIndicatorsToTags = (indicators_to_tags) => {
  const grouped_indicators_to_tags = _.groupBy(indicators_to_tags, 'indicator_tag_id')
  _.forEach(data.tag_index, tag => {
    tag.indicator_ids = _.map(grouped_indicators_to_tags[tag.id], 'indicator_id')
  })
}

export default indicators
