const OpenAI = require('openai');
const axios = require('axios');
const natural = require('natural');

class ComedyAgentOrchestrator {
  constructor() {
    this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    this.agents = {
      topical: new TopicalHumorAgent(this.openai),
      observational: new ObservationalComedyAgent(this.openai),
      wordplay: new WordplayAgent(this.openai),
      story: new StoryAgent(this.openai),
      meme: new MemeAgent(this.openai)
    };
  }

  async generateContent(userPrompt, userPreferences, currentEvents) {
    const contentRequests = await this.planContentGeneration(userPrompt, userPreferences);
    const results = [];

    for (const request of contentRequests) {
      const agent = this.agents[request.agentType];
      const content = await agent.generate(request, currentEvents, userPreferences);
      results.push({
        content,
        agent: request.agentType,
        qualityScore: await this.scoreContent(content, userPreferences)
      });
    }

    return results.sort((a, b) => b.qualityScore - a.qualityScore);
  }

  async planContentGeneration(userPrompt, preferences) {
    const prompt = `
    Analyze this user request for comedy content: "${userPrompt}"
    User preferences: ${JSON.stringify(preferences.comedyProfile)}

    Determine which comedy agents should generate content and what specific requests to make.

    Available agents:
    - topical: Current events and trending topics humor
    - observational: Everyday life comedy
    - wordplay: Puns, word games, linguistic humor
    - story: Longer comedic narratives
    - meme: Visual humor concepts

    Return a JSON array of content requests:
    [
      {
        "agentType": "topical",
        "specificRequest": "Create a joke about today's trending topic X",
        "priority": 1,
        "format": "one-liner"
      }
    ]
    `;

    const response = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7
    });

    return JSON.parse(response.choices[0].message.content);
  }

  async scoreContent(content, userPreferences) {
    const comedyScore = await this.analyzeHumorQuality(content);
    const personalityMatch = await this.calculatePersonalityMatch(content, userPreferences);
    const originalityScore = await this.checkOriginality(content);

    return (comedyScore * 0.4 + personalityMatch * 0.4 + originalityScore * 0.2);
  }

  async analyzeHumorQuality(content) {
    const sentiment = new natural.SentimentAnalyzer('English', natural.PorterStemmer, 'afinn');
    const tokens = new natural.WordTokenizer().tokenize(content.text || '');
    const score = sentiment.getSentiment(tokens);
    return Math.min(Math.max((score + 5) / 10, 0), 1);
  }

  async calculatePersonalityMatch(content, userPreferences) {
    return Math.random() * 0.3 + 0.7;
  }

  async checkOriginality(content) {
    return Math.random() * 0.4 + 0.6;
  }
}

class TopicalHumorAgent {
  constructor(openai) {
    this.openai = openai;
    this.newsAPI = axios.create({
      baseURL: 'https://newsapi.org/v2',
      headers: { 'X-API-Key': process.env.NEWS_API_KEY }
    });
  }

  async generate(request, currentEvents, userPreferences) {
    const relevantNews = await this.getRelevantNews(userPreferences.favoriteTopics || []);

    const prompt = `
    Create ${request.format || 'observational'} comedy content based on:
    Request: ${request.specificRequest}
    Recent news: ${JSON.stringify(relevantNews.slice(0, 3))}
    User humor style: ${userPreferences.comedyProfile?.humorStyles?.join(', ') || 'general'}

    Guidelines:
    - Keep it respectful and non-offensive
    - Focus on absurdity and observation rather than mean-spirited humor
    - Make it relatable and current
    - Length: ${this.getTargetLength(request.format)}
    `;

    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.8,
        max_tokens: 300
      });

      return {
        text: response.choices[0].message.content,
        type: request.format || 'story',
        metadata: {
          newsSource: relevantNews[0]?.title || '',
          generationTime: new Date(),
          agent: 'topical'
        }
      };
    } catch (error) {
      console.error('Error generating topical humor:', error);
      return this.getFallbackContent(request);
    }
  }

  async getRelevantNews(topics) {
    try {
      if (!process.env.NEWS_API_KEY || process.env.NEWS_API_KEY === 'your-news-api-key') {
        return this.getMockNews();
      }

      const queries = topics.length ? topics : ['trending'];
      const newsPromises = queries.map(topic =>
        this.newsAPI.get('/everything', {
          params: {
            q: topic,
            sortBy: 'publishedAt',
            pageSize: 5,
            language: 'en'
          }
        })
      );

      const responses = await Promise.all(newsPromises);
      return responses.flatMap(response => response.data.articles);
    } catch (error) {
      console.error('Error fetching news:', error);
      return this.getMockNews();
    }
  }

  getMockNews() {
    return [
      { title: "AI Makes Coffee, Forgets to Add Water", source: "Tech Times" },
      { title: "Local Cat Elected Mayor in Surprise Write-In Campaign", source: "Daily News" },
      { title: "Scientists Discover Vegetables Have Been Plotting Against Us", source: "Science Weekly" }
    ];
  }

  getTargetLength(format) {
    const lengths = {
      'one-liner': '1-2 sentences',
      'story': '3-5 sentences',
      'meme': 'Caption under 20 words'
    };
    return lengths[format] || '2-3 sentences';
  }

  getFallbackContent(request) {
    return {
      text: "Why did the AI go to therapy? It had too many unresolved dependencies!",
      type: request.format || 'one-liner',
      metadata: {
        newsSource: '',
        generationTime: new Date(),
        agent: 'topical',
        fallback: true
      }
    };
  }
}

class ObservationalComedyAgent {
  constructor(openai) {
    this.openai = openai;
  }

  async generate(request, currentEvents, userPreferences) {
    const topics = [
      'working from home', 'social media habits', 'food delivery apps',
      'video calls', 'streaming services', 'smartphone addiction',
      'online shopping', 'dating apps', 'fitness trackers'
    ];

    const randomTopic = topics[Math.floor(Math.random() * topics.length)];

    const prompt = `
    Create observational comedy about: ${randomTopic}
    Request: ${request.specificRequest}
    Style: ${userPreferences.comedyProfile?.comedyPersonality || 'witty'}
    Format: ${request.format}

    Focus on:
    - Universal experiences everyone can relate to
    - Small absurdities of modern life
    - "Did you ever notice..." style observations
    - Keep it light and relatable
    `;

    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.7
      });

      return {
        text: response.choices[0].message.content,
        type: request.format || 'story',
        metadata: {
          topic: randomTopic,
          agent: 'observational'
        }
      };
    } catch (error) {
      console.error('Error generating observational comedy:', error);
      return {
        text: `Ever notice how we spend 20 minutes picking something to watch on Netflix, then just end up scrolling on our phones anyway? We're not watching shows anymore, we're just providing background noise for our doom scrolling.`,
        type: request.format || 'story',
        metadata: {
          topic: randomTopic,
          agent: 'observational',
          fallback: true
        }
      };
    }
  }
}

class WordplayAgent {
  constructor(openai) {
    this.openai = openai;
  }

  async generate(request, currentEvents, userPreferences) {
    const prompt = `
    Create clever wordplay or pun-based humor.
    Request: ${request.specificRequest}
    Format: ${request.format || 'one-liner'}

    Guidelines:
    - Use clever word combinations, puns, or linguistic humor
    - Can be dad jokes, but make them clever
    - Keep it short and punchy
    `;

    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.8
      });

      return {
        text: response.choices[0].message.content,
        type: request.format || 'one-liner',
        metadata: {
          agent: 'wordplay'
        }
      };
    } catch (error) {
      return {
        text: "I used to hate facial hair, but then it grew on me.",
        type: request.format || 'one-liner',
        metadata: {
          agent: 'wordplay',
          fallback: true
        }
      };
    }
  }
}

class StoryAgent {
  constructor(openai) {
    this.openai = openai;
  }

  async generate(request, currentEvents, userPreferences) {
    const prompt = `
    Create a short comedic story or anecdote.
    Request: ${request.specificRequest}
    Personality: ${userPreferences.comedyProfile?.comedyPersonality || 'witty'}

    Guidelines:
    - Build up to a funny conclusion
    - Include relatable characters or situations
    - Keep it under 5 sentences
    - Have a clear punchline or twist
    `;

    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.75
      });

      return {
        text: response.choices[0].message.content,
        type: 'story',
        metadata: {
          agent: 'story'
        }
      };
    } catch (error) {
      return {
        text: "My fitness tracker congratulated me on reaching my step goal. I was just pacing around trying to remember what I walked into the room for. Technology thinks my anxiety is exercise.",
        type: 'story',
        metadata: {
          agent: 'story',
          fallback: true
        }
      };
    }
  }
}

class MemeAgent {
  constructor(openai) {
    this.openai = openai;
  }

  async generate(request, currentEvents, userPreferences) {
    const memeTemplates = [
      'Drake meme', 'Distracted boyfriend', 'Woman yelling at cat',
      'This is fine', 'Expanding brain', 'Change my mind'
    ];

    const template = memeTemplates[Math.floor(Math.random() * memeTemplates.length)];

    const prompt = `
    Create meme text for the "${template}" format.
    Request: ${request.specificRequest}

    Return in format:
    Top text: [text]
    Bottom text: [text]

    Keep it short, punchy, and relatable.
    `;

    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.8
      });

      return {
        text: response.choices[0].message.content,
        type: 'meme',
        metadata: {
          template,
          agent: 'meme'
        }
      };
    } catch (error) {
      return {
        text: "Top text: Starting a new project\nBottom text: 47 open browser tabs of documentation",
        type: 'meme',
        metadata: {
          template,
          agent: 'meme',
          fallback: true
        }
      };
    }
  }
}

module.exports = { ComedyAgentOrchestrator };