import _ from 'lodash'

export default function treeify (data, idKey) {
  let index = _.indexBy(data, idKey)
  let roots = []

  for (let i = data.length - 1; i >= 0; i--) {
    let d = data[i]

    if (d.parent && index[d.parent]) {
      let p = index[d.parent]

      if (!p.children) {
        p.children = []
      }

      p.children.push(d)
    } else {
      roots.push(d)
    }
  }

  return roots
}
