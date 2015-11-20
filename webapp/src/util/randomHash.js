import Crypto from 'crypto'
export default function () {
  return Crypto.randomBytes(5).toString('hex')
}
