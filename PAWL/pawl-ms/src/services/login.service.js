const User = require('../models/user.model')

const login = async (email, password) => {
  const user = await User.findByCredentials(email, password)
  const accessToken = await user.generateAuthToken()
  return ({ user, accessToken })
}

module.exports = login
