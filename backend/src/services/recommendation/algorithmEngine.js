const User = require('../../models/User');
const Post = require('../../models/Post');

class RecommendationEngine {
  constructor() {
    this.userEmbeddings = new Map();
    this.contentEmbeddings = new Map();
  }

  async generateRecommendations(userId, limit = 20) {
    const user = await User.findById(userId).populate('behaviorData');
    const userProfile = await this.buildUserProfile(user);

    const collaborativeScores = await this.getCollaborativeRecommendations(userId, userProfile);
    const contentScores = await this.getContentBasedRecommendations(userId, userProfile);
    const trendingBoosts = await this.getTrendingBoosts();

    const combinedScores = this.combineScores(
      collaborativeScores,
      contentScores,
      trendingBoosts,
      { collaborative: 0.4, content: 0.4, trending: 0.2 }
    );

    return this.rankAndFilter(combinedScores, user, limit);
  }

  async buildUserProfile(user) {
    const recentInteractions = await this.getRecentInteractions(user._id);
    const engagementPatterns = this.analyzeEngagementPatterns(recentInteractions);

    return {
      demographics: {
        accountAge: Date.now() - user.createdAt,
        followingCount: user.following.length,
        followerCount: user.followers.length
      },
      preferences: user.comedyProfile,
      behavior: {
        timeSpentOnTypes: user.behaviorData.timeSpentOnTypes,
        averageSessionLength: this.calculateAverageSession(recentInteractions),
        peakActivityHours: this.findPeakHours(recentInteractions),
        engagementVelocity: engagementPatterns.velocity,
        contentPreferenceScores: engagementPatterns.contentScores
      },
      socialSignals: {
        similarUsers: await this.findSimilarUsers(user._id),
        influenceScore: this.calculateInfluenceScore(user),
        communityAlignment: this.calculateCommunityAlignment(user)
      }
    };
  }

  async getCollaborativeRecommendations(userId, userProfile) {
    const similarUsers = await this.findSimilarUsersByBehavior(userId, userProfile);
    const recommendations = new Map();

    for (const similarUser of similarUsers) {
      const theirLikedPosts = await this.getUserLikedPosts(similarUser.userId);
      const similarity = similarUser.similarity;

      for (const post of theirLikedPosts) {
        if (!recommendations.has(post._id.toString())) {
          recommendations.set(post._id.toString(), 0);
        }
        const currentScore = recommendations.get(post._id.toString());
        recommendations.set(post._id.toString(),
          currentScore + similarity * (post.engagementScore || 1)
        );
      }
    }

    return recommendations;
  }

  async getContentBasedRecommendations(userId, userProfile) {
    const userInteractionHistory = await this.getUserInteractionHistory(userId);
    const preferredFeatures = this.extractContentFeatures(userInteractionHistory);

    const candidatePosts = await Post.find({
      author: { $ne: userId },
      moderationStatus: { $ne: 'removed' },
      createdAt: { $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) }
    }).populate('author', 'username profileImage').limit(100);

    const scoredPosts = new Map();

    for (const post of candidatePosts) {
      const contentFeatures = this.extractPostFeatures(post);
      const similarity = this.calculateContentSimilarity(preferredFeatures, contentFeatures);
      const freshness = this.calculateFreshnessScore(post.createdAt);
      const quality = post.qualityScores?.comedyRating || 5;

      const score = similarity * 0.6 + freshness * 0.2 + (quality / 10) * 0.2;
      scoredPosts.set(post._id.toString(), score);
    }

    return scoredPosts;
  }

  async getTrendingBoosts() {
    const trending = await Post.aggregate([
      {
        $match: {
          createdAt: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) },
          moderationStatus: { $ne: 'removed' }
        }
      },
      {
        $addFields: {
          engagementScore: {
            $add: [
              { $size: { $ifNull: ['$engagement.likes', []] } },
              { $multiply: [{ $size: { $ifNull: ['$engagement.laughReacts', []] } }, 1.5] },
              { $multiply: [{ $size: { $ifNull: ['$engagement.shares', []] } }, 2] },
              { $multiply: [{ $size: { $ifNull: ['$engagement.saves', []] } }, 1.2] }
            ]
          },
          viralVelocity: {
            $divide: [
              { $ifNull: ['$performance.views', 0] },
              { $max: [{ $divide: [{ $subtract: [new Date(), '$createdAt'] }, 3600000] }, 1] }
            ]
          }
        }
      },
      {
        $sort: { viralVelocity: -1, engagementScore: -1 }
      },
      {
        $limit: 50
      }
    ]);

    const boosts = new Map();
    trending.forEach((post, index) => {
      const boost = Math.max(0, 1 - (index / 50));
      boosts.set(post._id.toString(), boost);
    });

    return boosts;
  }

  combineScores(collaborative, contentBased, trending, weights) {
    const combined = new Map();
    const allPostIds = new Set([
      ...collaborative.keys(),
      ...contentBased.keys(),
      ...trending.keys()
    ]);

    for (const postId of allPostIds) {
      const collabScore = collaborative.get(postId) || 0;
      const contentScore = contentBased.get(postId) || 0;
      const trendingScore = trending.get(postId) || 0;

      const finalScore =
        collabScore * weights.collaborative +
        contentScore * weights.content +
        trendingScore * weights.trending;

      combined.set(postId, finalScore);
    }

    return combined;
  }

  async rankAndFilter(scoredPosts, user, limit) {
    const sortedPosts = Array.from(scoredPosts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit * 2);

    const diversePosts = this.ensureDiversity(sortedPosts, user.comedyProfile);
    const finalPosts = await this.addPostDetails(diversePosts.slice(0, limit));

    return finalPosts;
  }

  ensureDiversity(sortedPosts, userPreferences) {
    const diverse = [];
    const typesSeen = new Set();
    const authorsSeen = new Set();
    const maxPerType = 3;
    const maxPerAuthor = 2;

    for (const [postId, score] of sortedPosts) {
      if (diverse.length >= 20) break;
      diverse.push([postId, score]);
    }

    return diverse;
  }

  async addPostDetails(postIds) {
    const posts = await Post.find({
      _id: { $in: postIds.map(([id]) => id) }
    }).populate('author', 'username profileImage comedyProfile');

    return posts;
  }

  calculateContentSimilarity(features1, features2) {
    if (!features1 || !features2) return 0;

    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;

    for (const key in features1) {
      if (features2[key] !== undefined) {
        dotProduct += features1[key] * features2[key];
      }
      norm1 += features1[key] * features1[key];
    }

    for (const key in features2) {
      norm2 += features2[key] * features2[key];
    }

    if (norm1 === 0 || norm2 === 0) return 0;
    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }

  extractContentFeatures(posts) {
    const features = {
      meme: 0,
      story: 0,
      video: 0,
      'one-liner': 0,
      observational: 0,
      dark: 0,
      wordplay: 0
    };

    if (!posts || posts.length === 0) return features;

    posts.forEach(post => {
      if (post.type) features[post.type] = (features[post.type] || 0) + 1;
      if (post.comedyMetadata?.humorStyle) {
        features[post.comedyMetadata.humorStyle] = (features[post.comedyMetadata.humorStyle] || 0) + 1;
      }
    });

    const total = Object.values(features).reduce((a, b) => a + b, 0);
    if (total > 0) {
      Object.keys(features).forEach(key => {
        features[key] = features[key] / total;
      });
    }

    return features;
  }

  extractPostFeatures(post) {
    const features = {};

    if (post.type) features[post.type] = 1;
    if (post.comedyMetadata?.humorStyle) features[post.comedyMetadata.humorStyle] = 1;

    features.hasImage = post.content?.image ? 1 : 0;
    features.hasVideo = post.content?.video ? 1 : 0;
    features.textLength = post.content?.text ? Math.min(post.content.text.length / 500, 1) : 0;

    return features;
  }

  calculateFreshnessScore(createdAt) {
    const hoursOld = (Date.now() - new Date(createdAt)) / (1000 * 60 * 60);
    return Math.max(0, 1 - (hoursOld / 168));
  }

  calculateInfluenceScore(user) {
    const followers = user.followers?.length || 0;
    const engagement = user.engagementMetrics?.avgEngagementRate || 0;
    return Math.log10(followers + 1) * engagement;
  }

  calculateCommunityAlignment(user) {
    return 0.5;
  }

  async getRecentInteractions(userId) {
    const posts = await Post.find({
      'engagement.likes.user': userId
    }).limit(50).sort('-createdAt');
    return posts;
  }

  analyzeEngagementPatterns(interactions) {
    return {
      velocity: interactions.length / 50,
      contentScores: this.extractContentFeatures(interactions)
    };
  }

  calculateAverageSession(interactions) {
    return 30;
  }

  findPeakHours(interactions) {
    return [14, 20];
  }

  async findSimilarUsers(userId) {
    const user = await User.findById(userId);
    if (!user) return [];

    const similarUsers = await User.find({
      _id: { $ne: userId },
      'comedyProfile.humorStyles': { $in: user.comedyProfile?.humorStyles || [] }
    }).limit(10);

    return similarUsers.map(u => u._id);
  }

  async findSimilarUsersByBehavior(userId, userProfile) {
    const similarUserIds = userProfile.socialSignals?.similarUsers || [];

    return similarUserIds.map(id => ({
      userId: id,
      similarity: Math.random() * 0.3 + 0.7
    }));
  }

  async getUserLikedPosts(userId) {
    const posts = await Post.find({
      'engagement.likes.user': userId
    }).limit(20).sort('-createdAt');

    return posts.map(post => ({
      _id: post._id,
      engagementScore:
        (post.engagement?.likes?.length || 0) +
        (post.engagement?.laughReacts?.length || 0) * 1.5 +
        (post.engagement?.shares?.length || 0) * 2
    }));
  }

  async getUserInteractionHistory(userId) {
    return await Post.find({
      $or: [
        { 'engagement.likes.user': userId },
        { 'engagement.laughReacts.user': userId },
        { 'engagement.shares.user': userId },
        { 'engagement.saves.user': userId }
      ]
    }).limit(100).sort('-createdAt');
  }
}

module.exports = RecommendationEngine;