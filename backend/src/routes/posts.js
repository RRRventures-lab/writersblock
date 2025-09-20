const express = require('express');
const router = express.Router();
const Post = require('../models/Post');

router.get('/', async (req, res) => {
  try {
    const { type, limit = 20, offset = 0 } = req.query;

    let query = { moderationStatus: { $ne: 'removed' } };

    if (type === 'following') {
      const user = await req.user.populate('following');
      query.author = { $in: user.following };
    } else if (type === 'trending') {
      const posts = await Post.aggregate([
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
                { $multiply: [{ $size: { $ifNull: ['$engagement.shares', []] } }, 2] }
              ]
            }
          }
        },
        { $sort: { engagementScore: -1 } },
        { $skip: parseInt(offset) },
        { $limit: parseInt(limit) }
      ]);

      await Post.populate(posts, {
        path: 'author',
        select: 'username profileImage'
      });

      return res.json(posts);
    }

    const posts = await Post.find(query)
      .populate('author', 'username profileImage')
      .sort('-createdAt')
      .skip(parseInt(offset))
      .limit(parseInt(limit));

    res.json(posts);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post('/', async (req, res) => {
  try {
    const { content, type, comedyMetadata, hashtags } = req.body;

    const post = await Post.create({
      author: req.user._id,
      content,
      type,
      comedyMetadata,
      hashtags,
      moderationStatus: 'approved'
    });

    await post.populate('author', 'username profileImage');

    res.status(201).json(post);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post('/:id/like', async (req, res) => {
  try {
    const post = await Post.findById(req.params.id);

    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    const alreadyLiked = post.engagement.likes.some(
      like => like.user.toString() === req.user._id.toString()
    );

    if (alreadyLiked) {
      post.engagement.likes = post.engagement.likes.filter(
        like => like.user.toString() !== req.user._id.toString()
      );
    } else {
      post.engagement.likes.push({ user: req.user._id });
    }

    await post.save();
    res.json(post);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post('/:id/laugh', async (req, res) => {
  try {
    const { intensity } = req.body;
    const post = await Post.findById(req.params.id);

    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    const existingLaugh = post.engagement.laughReacts.findIndex(
      react => react.user.toString() === req.user._id.toString()
    );

    if (existingLaugh !== -1) {
      post.engagement.laughReacts[existingLaugh].intensity = intensity;
    } else {
      post.engagement.laughReacts.push({ user: req.user._id, intensity });
    }

    await post.save();
    res.json(post);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;