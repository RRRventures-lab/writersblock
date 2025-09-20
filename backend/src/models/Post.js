const mongoose = require('mongoose');

const postSchema = new mongoose.Schema({
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  content: {
    text: String,
    image: String,
    video: String,
    memeTemplate: String
  },
  type: {
    type: String,
    enum: ['meme', 'story', 'video', 'one-liner', 'sketch', 'ai-generated'],
    required: true
  },
  isAIGenerated: {
    type: Boolean,
    default: false
  },
  aiMetadata: {
    generatingAgent: String,
    prompt: String,
    currentEventTrigger: String,
    qualityScore: Number,
    styleEmulated: String
  },
  comedyMetadata: {
    humorStyle: String,
    topics: [String],
    complexity: {
      type: String,
      enum: ['simple', 'moderate', 'complex']
    },
    targetAudience: String,
    culturalReferences: [String]
  },
  engagement: {
    likes: [{
      user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
      timestamp: { type: Date, default: Date.now }
    }],
    laughReacts: [{
      user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
      intensity: { type: Number, min: 1, max: 5 },
      timestamp: { type: Date, default: Date.now }
    }],
    shares: [{
      user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
      timestamp: { type: Date, default: Date.now }
    }],
    saves: [{
      user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
      timestamp: { type: Date, default: Date.now }
    }]
  },
  comments: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Comment'
  }],
  hashtags: [String],
  mentions: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  visibility: {
    type: String,
    enum: ['public', 'followers', 'private'],
    default: 'public'
  },
  moderationStatus: {
    type: String,
    enum: ['pending', 'approved', 'flagged', 'removed'],
    default: 'pending'
  },
  qualityScores: {
    comedyRating: { type: Number, min: 0, max: 10 },
    originalityScore: { type: Number, min: 0, max: 10 },
    engagementPrediction: { type: Number, min: 0, max: 10 }
  },
  performance: {
    views: { type: Number, default: 0 },
    completionRate: { type: Number, default: 0 },
    timeSpent: { type: Number, default: 0 },
    viralScore: { type: Number, default: 0 }
  }
}, {
  timestamps: true
});

postSchema.index({ author: 1, createdAt: -1 });
postSchema.index({ type: 1, 'comedyMetadata.humorStyle': 1 });
postSchema.index({ hashtags: 1 });
postSchema.index({ 'qualityScores.comedyRating': -1 });

module.exports = mongoose.model('Post', postSchema);