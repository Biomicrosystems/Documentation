const express = require('express')
const log = require('../services/logger.service')

const router = new express.Router()

router.post('/', async (req, res) => {
  const { body } = req
  log.info(body.info)
  res.status(201).send(body)
})

module.exports = router
