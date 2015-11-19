export default function (name) {
  function model (data) {
    let series = {
      points: data
    }

    if (name) {
      series.name = typeof name === 'function' ? name(data) : name
    }
    return series
  }

  return model
}
