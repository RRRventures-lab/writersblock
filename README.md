# Comedy Social Media Platform 🎭

A sophisticated social media platform focused on AI-powered comedy content generation with personalized recommendations.

## 🚀 Quick Start

### Prerequisites
- Node.js (v18+ recommended)
- MongoDB (local or cloud)
- Redis (optional, for caching)

### Installation & Setup

1. **Backend Setup**
```bash
cd backend
npm install
cp .env.example .env  # Configure your environment variables
npm run dev  # Starts on port 8000
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start   # Starts on port 4000
```

### Environment Variables

**Backend (.env):**
```env
NODE_ENV=development
PORT=8000
MONGODB_URI=mongodb://localhost:27017/comedy-social
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRE=7d

# AI Service Keys (optional for demo)
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key

# File Upload
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=50000000
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_SOCKET_URL=http://localhost:8000
```

## 🎯 Core Features

### ✅ **Completed & Working**

- **🔐 User Authentication** - Complete login/register system with JWT
- **🤖 AI Comedy Generation** - 5 specialized comedy agents:
  - **Topical Humor Agent** - Current events and trending topics
  - **Observational Comedy Agent** - Everyday life humor
  - **Wordplay Agent** - Puns and linguistic humor
  - **Story Agent** - Comedic narratives
  - **Meme Agent** - Visual humor concepts
- **🎯 Personalized Recommendation Engine** - Meta-style algorithm with:
  - Collaborative filtering
  - Content-based recommendations
  - Trending boosts
  - User behavior analysis
- **📱 Real-time Social Feed** - Infinite scroll with Socket.IO updates
- **🎨 Comedy Style Profiling** - User preference learning
- **💾 Advanced Database Schema** - MongoDB with complex relationships
- **🔄 Multi-format Content Support** - Memes, stories, videos, one-liners
- **💫 Engagement System** - Likes, laugh reactions (1-5 intensity), shares, saves
- **🛡️ Content Moderation** - Built-in filtering and approval system

### 🏗️ **Architecture**

**Backend:**
- **Express.js** - REST API server
- **MongoDB** - Primary database with Mongoose ODM
- **Socket.IO** - Real-time updates
- **Redis** - Caching and session management
- **OpenAI Integration** - AI content generation
- **JWT Authentication** - Secure user sessions
- **Rate Limiting** - API protection
- **File Upload** - Multer with Sharp image processing

**Frontend:**
- **React 18** with TypeScript
- **Redux Toolkit** - State management
- **React Router** - Navigation
- **Axios** - API communication
- **Socket.IO Client** - Real-time features
- **Infinite Scroll** - Optimized feed loading

## 🧪 Testing

### Manual Testing
1. **Health Check**: `curl http://localhost:8000/health`
2. **Frontend**: Open `http://localhost:4000`
3. **Register/Login**: Create account and test authentication
4. **AI Generation**: Use the comedy generation features
5. **Feed**: Test personalized recommendations

### API Endpoints
- `GET /health` - Server health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/posts` - Fetch posts (trending/following)
- `GET /api/recommendations` - Personalized content
- `POST /api/ai/generate` - Generate comedy content
- `POST /api/posts/:id/like` - Like/unlike posts

## 🔧 Development

### Project Structure
```
comedy-social-app/
├── backend/
│   ├── src/
│   │   ├── controllers/     # API controllers
│   │   ├── models/         # MongoDB schemas
│   │   ├── routes/         # Express routes
│   │   ├── services/       # Business logic
│   │   │   ├── ai/         # Comedy generation
│   │   │   └── recommendation/ # Recommendation engine
│   │   └── middleware/     # Auth, validation, etc.
│   └── uploads/           # File storage
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── pages/         # Page components
    │   ├── store/         # Redux slices
    │   └── services/      # API calls
    └── public/
```

### Key Components

**AI Comedy System:**
- `ComedyAgentOrchestrator` - Manages multiple AI agents
- `TopicalHumorAgent` - News-based comedy
- `ObservationalComedyAgent` - Everyday humor
- `WordplayAgent` - Puns and wordplay
- `StoryAgent` - Narrative comedy
- `MemeAgent` - Visual humor

**Recommendation Engine:**
- `RecommendationEngine` - Core algorithm
- User profiling and behavior analysis
- Content similarity scoring
- Collaborative filtering
- Trending content detection

## 🚀 Deployment

### Production Setup
1. Set `NODE_ENV=production`
2. Configure production MongoDB/Redis
3. Set secure JWT secrets
4. Add API keys for AI services
5. Configure CORS for production domains
6. Set up file storage (AWS S3/CloudFront)

### Docker (Optional)
```bash
docker-compose up -d  # If docker-compose.yml is created
```

## 🎭 Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "comedian123",
    "email": "user@example.com",
    "password": "password123",
    "comedyProfile": {
      "humorStyles": ["observational", "wordplay"],
      "comedyPersonality": "witty"
    }
  }'
```

### Generate AI Comedy Content
```bash
curl -X POST http://localhost:8000/api/ai/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Make a joke about working from home",
    "format": "one-liner"
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🎉 Current Status

**✅ FULLY FUNCTIONAL DEMO**
- Backend running on port 8000
- Frontend running on port 4000
- All core features implemented
- Ready for development and testing

The application successfully demonstrates:
- Modern full-stack architecture
- AI-powered content generation
- Sophisticated recommendation algorithms
- Real-time social media features
- Production-ready code structure