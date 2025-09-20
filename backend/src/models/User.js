const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    minlength: 3,
    maxlength: 30
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  profileImage: {
    type: String,
    default: ''
  },
  bio: {
    type: String,
    maxlength: 500
  },
  comedyProfile: {
    humorStyles: [{
      type: String,
      enum: ['observational', 'dark', 'wordplay', 'physical', 'surreal', 'political', 'self-deprecating']
    }],
    favoriteTopics: [String],
    preferredFormats: [{
      type: String,
      enum: ['memes', 'stories', 'videos', 'one-liners', 'sketches']
    }],
    comedyPersonality: {
      type: String,
      enum: ['witty', 'silly', 'sarcastic', 'wholesome', 'edgy']
    },
    customPrompts: [String]
  },
  preferences: {
    autoGenerateContent: {
      type: Boolean,
      default: true
    },
    contentFrequency: {
      type: String,
      enum: ['low', 'medium', 'high'],
      default: 'medium'
    },
    aiPersonalization: {
      type: Boolean,
      default: true
    }
  },
  followers: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  following: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  engagementMetrics: {
    totalLikes: { type: Number, default: 0 },
    totalShares: { type: Number, default: 0 },
    totalComments: { type: Number, default: 0 },
    avgEngagementRate: { type: Number, default: 0 }
  },
  behaviorData: {
    timeSpentOnTypes: {
      memes: { type: Number, default: 0 },
      stories: { type: Number, default: 0 },
      videos: { type: Number, default: 0 }
    },
    interactionPatterns: [{
      action: String,
      contentType: String,
      timestamp: { type: Date, default: Date.now }
    }],
    lastAnalyzed: { type: Date, default: Date.now }
  }
}, {
  timestamps: true
});

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

userSchema.methods.correctPassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);