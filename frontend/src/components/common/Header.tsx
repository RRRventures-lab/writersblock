import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/authSlice';
import { RootState, AppDispatch } from '../../store';
import { PlusIcon, UserIcon, ArrowLeftOnRectangleIcon } from '@heroicons/react/24/outline';

export const Header: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Comedy Social
          </h1>
        </div>

        <nav className="flex items-center space-x-4">
          <button className="bg-purple-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-purple-700 transition-colors">
            <PlusIcon className="w-5 h-5" />
            <span>Create Post</span>
          </button>

          <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <UserIcon className="w-6 h-6 text-gray-600" />
          </button>

          <button
            onClick={handleLogout}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <ArrowLeftOnRectangleIcon className="w-6 h-6 text-gray-600" />
          </button>
        </nav>
      </div>
    </header>
  );
};