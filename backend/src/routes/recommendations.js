const express = require('express');
const router = express.Router();
const RecommendationEngine = require('../services/recommendation/algorithmEngine');

const recommendationEngine = new RecommendationEngine();

router.get('/', async (req, res) => {
  try {
    const { limit = 20 } = req.query;
    const userId = req.user._id;

    const recommendations = await recommendationEngine.generateRecommendations(
      userId,
      parseInt(limit)
    );

    res.json(recommendations);
  } catch (error) {
    console.error('Recommendation error:', error);
    res.status(500).json({ message: 'Failed to generate recommendations' });
  }
});

router.post('/feedback', async (req, res) => {
  try {
    const { postId, action, duration } = req.body;
    const userId = req.user._id;

    await req.user.updateOne({
      $push: {
        'behaviorData.interactionPatterns': {
          action,
          contentType: postId,
          timestamp: new Date()
        }
      }
    });

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;