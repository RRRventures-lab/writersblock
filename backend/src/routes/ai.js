const express = require('express');
const router = express.Router();
const { ComedyAgentOrchestrator } = require('../services/ai/comedyAgents');
const Post = require('../models/Post');

const comedyOrchestrator = new ComedyAgentOrchestrator();

router.post('/generate', async (req, res) => {
  try {
    const { prompt, format } = req.body;
    const userPreferences = req.user;

    const results = await comedyOrchestrator.generateContent(
      prompt,
      userPreferences,
      []
    );

    res.json(results);
  } catch (error) {
    console.error('AI generation error:', error);
    res.status(500).json({ message: 'Failed to generate content' });
  }
});

router.post('/generate-and-post', async (req, res) => {
  try {
    const { prompt, format, autoPost } = req.body;
    const userPreferences = req.user;

    const results = await comedyOrchestrator.generateContent(
      prompt,
      userPreferences,
      []
    );

    if (results.length === 0) {
      return res.status(400).json({ message: 'No content generated' });
    }

    const bestContent = results[0];

    if (autoPost) {
      const post = await Post.create({
        author: req.user._id,
        content: {
          text: bestContent.content.text
        },
        type: bestContent.content.type || 'ai-generated',
        isAIGenerated: true,
        aiMetadata: {
          generatingAgent: bestContent.agent,
          prompt: prompt,
          qualityScore: bestContent.qualityScore
        },
        comedyMetadata: {
          humorStyle: userPreferences.comedyProfile?.humorStyles?.[0] || 'general'
        },
        moderationStatus: 'approved'
      });

      await post.populate('author', 'username profileImage');
      res.json({ generated: bestContent, post });
    } else {
      res.json({ generated: bestContent });
    }
  } catch (error) {
    console.error('AI generation error:', error);
    res.status(500).json({ message: 'Failed to generate content' });
  }
});

module.exports = router;