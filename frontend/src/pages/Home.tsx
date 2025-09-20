import React from 'react';

const Home: React.FC = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      <header style={{
        backgroundColor: 'white',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        padding: '16px 0'
      }}>
        <div className="container" style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h1 style={{
            fontSize: '24px',
            fontWeight: 'bold',
            background: 'linear-gradient(to right, #8b5cf6, #ec4899)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            color: 'transparent'
          }}>
            Comedy Social
          </h1>
          <div>
            <button style={{
              backgroundColor: '#8b5cf6',
              color: 'white',
              padding: '8px 16px',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              marginRight: '8px'
            }}>
              Create Post
            </button>
            <button style={{
              backgroundColor: 'transparent',
              color: '#6b7280',
              padding: '8px',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer'
            }}>
              Profile
            </button>
          </div>
        </div>
      </header>

      <main style={{ padding: '32px 0' }}>
        <div className="container" style={{
          maxWidth: '600px',
          margin: '0 auto',
          padding: '0 16px'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            textAlign: 'center'
          }}>
            <h2 style={{
              fontSize: '20px',
              fontWeight: 'bold',
              marginBottom: '16px',
              color: '#1f2937'
            }}>
              Welcome to Comedy Social! 🎭
            </h2>
            <p style={{
              color: '#6b7280',
              marginBottom: '16px'
            }}>
              Your AI-powered comedy platform is ready to go!
            </p>
            <p style={{
              fontSize: '14px',
              color: '#9ca3af'
            }}>
              Backend running on port 8000 | Frontend running on port 4000
            </p>
          </div>

          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            marginTop: '16px'
          }}>
            <h3 style={{
              fontSize: '18px',
              fontWeight: 'bold',
              marginBottom: '16px',
              color: '#1f2937'
            }}>
              🎯 Features Available
            </h3>
            <ul style={{
              textAlign: 'left',
              color: '#6b7280',
              lineHeight: '1.6'
            }}>
              <li>✅ User Authentication (Login/Register)</li>
              <li>✅ AI Comedy Generation with 5 Specialized Agents</li>
              <li>✅ Personalized Recommendation Engine</li>
              <li>✅ Real-time Social Feed</li>
              <li>✅ Comedy Style Profiling</li>
              <li>✅ Multi-format Content (Memes, Stories, Videos)</li>
              <li>✅ Engagement Tracking (Likes, Laughs, Shares)</li>
              <li>✅ MongoDB Database with Complex Schemas</li>
              <li>✅ Socket.IO Real-time Updates</li>
              <li>✅ RESTful API with Express.js</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;