const express = require('express')
const log = require('../services/logger.service')
const login = require('../services/login.service')

const router = new express.Router()

router.post('/', async (req, res) => {
  const { email } = req.body
  const { password } = req.body
  try {
    const loginResponse = await login(email, password)
    log.info(`User ${loginResponse.user._id} successfully login`)
    res.send(loginResponse)
  } catch (error) {
    log.error(error.message)
    res.status(400).send({ errorMessage: error.message })
  }
})

module.exports = router
