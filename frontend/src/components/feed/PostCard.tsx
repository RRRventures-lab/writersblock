import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { HeartIcon, ChatBubbleLeftIcon, ShareIcon, BookmarkIcon } from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import { likePost, sharePost, savePost } from '../../store/postsSlice';
import { RootState, AppDispatch } from '../../store';

interface PostCardProps {
  post: {
    id: string;
    author: {
      id: string;
      username: string;
      profileImage: string;
    };
    content: {
      text?: string;
      image?: string;
      video?: string;
    };
    type: string;
    isAIGenerated: boolean;
    aiMetadata?: {
      generatingAgent: string;
      qualityScore: number;
      styleEmulated?: string;
    };
    engagement: {
      likes: any[];
      laughReacts: any[];
      shares: any[];
      saves: any[];
    };
    hashtags: string[];
    createdAt: string;
    comedyMetadata: {
      humorStyle: string;
      topics: string[];
    };
  };
  showAIBadge?: boolean;
}

export const PostCard: React.FC<PostCardProps> = ({ post, showAIBadge = false }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const [isExpanded, setIsExpanded] = useState(false);
  const [laughIntensity, setLaughIntensity] = useState(0);

  const isLiked = post.engagement?.likes?.some((like: any) => like.user === user?.id);
  const isSaved = post.engagement?.saves?.some((save: any) => save.user === user?.id);

  const handleLike = () => {
    dispatch(likePost(post.id));
  };

  const handleShare = () => {
    dispatch(sharePost(post.id));
    if (navigator.share) {
      navigator.share({
        title: `Comedy post by ${post.author.username}`,
        text: post.content.text?.substring(0, 100) + '...',
        url: `${window.location.origin}/post/${post.id}`
      });
    }
  };

  const handleSave = () => {
    dispatch(savePost(post.id));
  };

  const shouldTruncate = post.content.text && post.content.text.length > 300;
  const displayText = shouldTruncate && !isExpanded
    ? post.content.text?.substring(0, 300) + '...'
    : post.content.text;

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <div className="p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <img
            src={post.author.profileImage || '/default-avatar.png'}
            alt={post.author.username}
            className="w-10 h-10 rounded-full object-cover bg-gray-200"
          />
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-semibold text-gray-900">{post.author.username}</h3>
              {post.isAIGenerated && showAIBadge && (
                <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs px-2 py-1 rounded-full">
                  AI
                </span>
              )}
            </div>
            <p className="text-sm text-gray-500">
              {new Date(post.createdAt).toLocaleDateString()}
            </p>
          </div>
        </div>

        <div className="flex space-x-2">
          {post.comedyMetadata?.humorStyle && (
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
              {post.comedyMetadata.humorStyle}
            </span>
          )}
          <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full">
            {post.type}
          </span>
        </div>
      </div>

      <div className="px-4 pb-4">
        {post.content.text && (
          <div className="mb-4">
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {displayText}
            </p>
            {shouldTruncate && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-purple-600 hover:text-purple-700 text-sm font-medium mt-2"
              >
                {isExpanded ? 'Show less' : 'Read more'}
              </button>
            )}
          </div>
        )}

        {post.content.image && (
          <div className="mb-4 rounded-lg overflow-hidden">
            <img
              src={post.content.image}
              alt="Post content"
              className="w-full h-auto object-cover max-h-96"
            />
          </div>
        )}

        {post.hashtags && post.hashtags.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2">
            {post.hashtags.map((tag, index) => (
              <span
                key={index}
                className="text-purple-600 hover:text-purple-700 cursor-pointer text-sm"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {post.isAIGenerated && post.aiMetadata && (
          <div className="mb-4 p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border border-purple-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-purple-700">
                Generated by {post.aiMetadata.generatingAgent} agent
              </span>
              <span className="text-purple-600">
                Quality: {Math.round(post.aiMetadata.qualityScore * 10)}/10
              </span>
            </div>
          </div>
        )}
      </div>

      <div className="px-4 py-3 border-t border-gray-100">
        <div className="flex items-center justify-between">
          <button
            onClick={handleLike}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
              isLiked
                ? 'bg-red-50 text-red-600'
                : 'hover:bg-gray-50 text-gray-600'
            }`}
          >
            {isLiked ? (
              <HeartSolidIcon className="w-5 h-5" />
            ) : (
              <HeartIcon className="w-5 h-5" />
            )}
            <span className="text-sm font-medium">
              {post.engagement?.likes?.length || 0}
            </span>
          </button>

          <div className="flex items-center space-x-1">
            {[1, 2, 3, 4, 5].map((intensity) => (
              <button
                key={intensity}
                onClick={() => setLaughIntensity(intensity)}
                className={`w-8 h-8 rounded-full text-sm transition-all ${
                  laughIntensity >= intensity
                    ? 'bg-yellow-400 text-white scale-110'
                    : 'bg-gray-100 text-gray-400 hover:bg-yellow-100'
                }`}
              >
                😂
              </button>
            ))}
            <span className="text-sm text-gray-500 ml-2">
              {post.engagement?.laughReacts?.length || 0}
            </span>
          </div>

          <button className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-50 text-gray-600 transition-colors">
            <ChatBubbleLeftIcon className="w-5 h-5" />
            <span className="text-sm font-medium">Comment</span>
          </button>

          <button
            onClick={handleShare}
            className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-50 text-gray-600 transition-colors"
          >
            <ShareIcon className="w-5 h-5" />
            <span className="text-sm font-medium">
              {post.engagement?.shares?.length || 0}
            </span>
          </button>

          <button
            onClick={handleSave}
            className={`p-2 rounded-lg transition-colors ${
              isSaved
                ? 'bg-blue-50 text-blue-600'
                : 'hover:bg-gray-50 text-gray-600'
            }`}
          >
            <BookmarkIcon className={`w-5 h-5 ${isSaved ? 'fill-current' : ''}`} />
          </button>
        </div>
      </div>
    </div>
  );
};