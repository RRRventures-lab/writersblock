import React, { useEffect, useState, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import InfiniteScroll from 'react-infinite-scroll-component';
import { PostCard } from './PostCard';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { fetchFeed, fetchRecommendations } from '../../store/postsSlice';
import { RootState, AppDispatch } from '../../store';

export const FeedContainer: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { posts, isLoading, hasMore } = useSelector(
    (state: RootState) => state.posts
  );
  const { user } = useSelector((state: RootState) => state.auth);

  const [feedType, setFeedType] = useState<'recommended' | 'following' | 'trending'>('recommended');

  useEffect(() => {
    loadInitialFeed();
  }, [feedType, user]);

  const loadInitialFeed = useCallback(async () => {
    if (!user) return;

    try {
      switch (feedType) {
        case 'recommended':
          await dispatch(fetchRecommendations({
            userId: user.id,
            limit: 20
          }));
          break;
        case 'following':
          await dispatch(fetchFeed({
            type: 'following',
            limit: 20
          }));
          break;
        case 'trending':
          await dispatch(fetchFeed({
            type: 'trending',
            limit: 20
          }));
          break;
      }
    } catch (error) {
      console.error('Error loading feed:', error);
    }
  }, [dispatch, feedType, user]);

  const loadMorePosts = useCallback(async () => {
    if (isLoading || !hasMore || !user) return;

    try {
      switch (feedType) {
        case 'recommended':
          await dispatch(fetchRecommendations({
            userId: user.id,
            limit: 10,
            offset: posts.length
          }));
          break;
        case 'following':
          await dispatch(fetchFeed({
            type: 'following',
            limit: 10,
            offset: posts.length
          }));
          break;
        case 'trending':
          await dispatch(fetchFeed({
            type: 'trending',
            limit: 10,
            offset: posts.length
          }));
          break;
      }
    } catch (error) {
      console.error('Error loading more posts:', error);
    }
  }, [dispatch, feedType, user, posts.length, isLoading, hasMore]);

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <div className="flex justify-center mb-6">
        <div className="bg-white rounded-full p-1 shadow-lg">
          {(['recommended', 'following', 'trending'] as const).map((type) => (
            <button
              key={type}
              onClick={() => setFeedType(type)}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                feedType === type
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-600 hover:text-purple-600'
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {feedType === 'recommended' && (
        <div className="mb-6 p-4 bg-gradient-to-r from-purple-100 to-pink-100 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-purple-800">AI Comedy Assistant</h3>
              <p className="text-sm text-purple-600">
                Want fresh comedy content? Tell me what's on your mind!
              </p>
            </div>
            <button
              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Generate
            </button>
          </div>
        </div>
      )}

      <InfiniteScroll
        dataLength={posts.length}
        next={loadMorePosts}
        hasMore={hasMore}
        loader={<LoadingSpinner />}
        endMessage={
          <p className="text-center text-gray-500 py-8">
            {posts.length === 0
              ? "No posts yet! Follow some comedians or create your first post."
              : "You've reached the end! Check back later for more laughs."}
          </p>
        }
      >
        <div className="space-y-6">
          {posts.map((post: any, index: number) => (
            <PostCard
              key={`${post._id || post.id}-${index}`}
              post={{
                ...post,
                id: post._id || post.id
              }}
              showAIBadge={feedType === 'recommended'}
            />
          ))}
        </div>
      </InfiniteScroll>
    </div>
  );
};