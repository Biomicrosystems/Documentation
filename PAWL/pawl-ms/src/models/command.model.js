const mongoose = require('mongoose')

const commandSchema = new mongoose.Schema({
  name: {
    type: String,
    trim: true,
    default: 'STOPPED_MEASUREMENT'
  },
  identifier: {
    type: String,
    trim: true,
    unique: true
  },
  deviceId: {
    type: String,
    trim: true,
    unique: true
  }
}, {
  timestamps: true
})

const Command = mongoose.model('Command', commandSchema)

module.exports = Command
