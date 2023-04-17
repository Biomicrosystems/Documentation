/* eslint-disable no-underscore-dangle */
const express = require('express')
const User = require('../models/user.model')
const log = require('../services/logger.service')
const createUser = require('../services/register.service')

const router = new express.Router()

router.post('/', async (req, res) => {
  const user = new User(req.body)
  try {
    const createdUser = await createUser(user)
    res.status(201).send(createdUser)
    log.info(`User ${createdUser.user._id} created successfully`)
  } catch (error) {
    log.error(error.message)
    res.status(400).send({ errorMessage: error.message })
  }
})

module.exports = router
