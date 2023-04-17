const createUser = async (user) => {
  await user.save()
  const accessToken = await user.generateAuthToken()
  return ({ user, accessToken })
}

module.exports = createUser
