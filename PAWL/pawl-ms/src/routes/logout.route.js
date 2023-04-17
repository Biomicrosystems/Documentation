const express = require('express')
const log = require('../services/logger.service')
const authenticate = require('../middleware/security.auth')

const router = new express.Router()

router.post('/', authenticate, async (req, res) => {
  try {
    req.user.token = ''
    await req.user.save()
    log.info('Logged Out Successfully')
    res.send({ message: 'Logged Out Successfully' })
  } catch (error) {
    res.status(500).send(error.message)
  }
})

module.exports = router
