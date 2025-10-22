# InvestIQ - Resume Context

## One-Line Description
AI-enhanced investment research platform with React + TypeScript frontend and Python FastAPI backend, deployed on Vercel + Render

## For Resume "Projects" Section

### Option 1: Concise (2-3 lines)
**InvestIQ** - AI-Enhanced Investment Research Platform
- Built full-stack app with React 18 + TypeScript frontend and Python FastAPI backend integrating 5 real-time data APIs
- Implemented Google Gemini AI for cross-signal analysis and pattern recognition with smart caching (80% cost reduction)
- Deployed production-ready application on Vercel + Render with CI/CD pipeline ($0 hosting cost)
- **Tech:** React, TypeScript, Python, FastAPI, Gemini AI, Vercel, Render
- **Live:** https://invest-iq-wheat.vercel.app

### Option 2: Detailed (4-5 lines)
**InvestIQ** - Full-Stack AI Investment Research Platform
[Oct 2025] | Live Demo: https://invest-iq-wheat.vercel.app
- Architected and deployed full-stack application with React 18 + TypeScript frontend (shadcn/ui) and Python FastAPI backend
- Integrated 5 real-time APIs (yfinance, NewsAPI, Reddit, Google Trends, Fear & Greed Index) with async parallel fetching for 3x speed improvement
- Implemented Google Gemini AI for advanced pattern recognition and cross-signal analysis; designed smart caching system reducing API costs by 80%
- Calculated technical indicators (RSI, moving averages, volume analysis) from scratch; built sentiment aggregation engine
- Deployed production-ready app using split architecture (Vercel for React, Render for Python) with infrastructure as code and CI/CD
- **Tech Stack:** React 18, TypeScript, Vite, Tailwind CSS, Python 3.11, FastAPI, Gemini AI, Recharts, Framer Motion
- **DevOps:** Vercel, Render, GitHub Actions, CORS configuration, environment management

### Option 3: Bullet Points for Resume
**InvestIQ - AI Investment Research Platform** | Oct 2025 | https://invest-iq-wheat.vercel.app
- Developed full-stack investment research platform aggregating real-time data from 5 APIs with React 18 + TypeScript frontend and Python FastAPI backend
- Integrated Google Gemini AI for pattern recognition and cross-signal analysis; implemented caching strategy reducing API costs 80%
- Built technical analysis engine calculating RSI, moving averages, and volume indicators; created weighted sentiment scoring system
- Deployed production application using split architecture: Vercel (React) + Render (Python) with CI/CD auto-deployment
- Optimized performance with async/await parallel data fetching (3x speed improvement) and comprehensive error handling
- **Technologies:** React, TypeScript, Python, FastAPI, Gemini AI, Tailwind CSS, shadcn/ui, Recharts, Vercel, Render

## For LinkedIn

### Headline Addition
Full-Stack Developer | AI Integration Specialist | Built InvestIQ - Production AI Research Platform

### Featured Project Description
**InvestIQ - AI-Enhanced Investment Research Platform**

🚀 Live: https://invest-iq-wheat.vercel.app
📁 GitHub: https://github.com/arjitmat/InvestIQ

I built a full-stack investment research platform that aggregates real-time market data from multiple sources and uses Google Gemini AI for enhanced analysis.

**Key Features:**
✅ React 18 + TypeScript frontend with shadcn/ui components
✅ Python FastAPI backend with async data fetching
✅ Google Gemini AI integration for pattern recognition
✅ 5 real-time data sources (yfinance, NewsAPI, Reddit, Trends, Fear & Greed)
✅ Technical analysis engine (RSI, MAs, volume analysis)
✅ Production deployment on Vercel + Render ($0 cost)

**Technical Highlights:**
🔹 Async parallel API fetching → 3x speed improvement
🔹 Smart caching with TTL → 80% cost reduction
🔹 Infrastructure as Code (render.yaml)
🔹 CI/CD pipeline with auto-deployment
🔹 Graceful degradation and comprehensive error handling

**Challenges Overcome:**
🎯 Hit Vercel's 50MB serverless limit → learned to choose right platform for each service
🎯 AI response inconsistencies → implemented robust JSON extraction and retry logic
🎯 API rate limits → designed transparent confidence levels and fallback strategies

This project demonstrates my ability to:
- Architect and deploy production-ready applications
- Integrate AI thoughtfully (not just API calls)
- Optimize for performance and cost
- Handle real-world deployment challenges
- Write clean, maintainable, documented code

**Tech Stack:**
Frontend: React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, Recharts, Framer Motion
Backend: Python 3.11, FastAPI, Uvicorn
AI: Google Gemini 2.0 Flash
Deployment: Vercel (frontend), Render (backend)

Try it out and let me know what you think! 🚀

#FullStackDevelopment #AI #MachineLearning #React #Python #FastAPI #WebDevelopment #Portfolio

## For Cover Letters

### Paragraph 1: Project Introduction
> I recently built InvestIQ, a production-ready AI-enhanced investment research platform that demonstrates my full-stack development capabilities. The application aggregates real-time market data from five different APIs, performs technical analysis, and uses Google Gemini AI for advanced pattern recognition. I deployed it using a modern split architecture with React on Vercel and Python on Render, implementing CI/CD pipelines and infrastructure as code.

### Paragraph 2: Technical Depth
> On the technical side, I architected a React 18 + TypeScript frontend with shadcn/ui components and a Python FastAPI backend that uses async/await for parallel data fetching, improving performance by 3x. The AI integration includes smart caching that reduced API costs by 80%, and I implemented graceful degradation patterns so the application remains functional even when individual data sources fail. The entire project costs $0 to host while maintaining full production functionality.

### Paragraph 3: Problem Solving
> During deployment, I encountered Vercel's 50MB serverless function limit for the Python backend due to pandas and numpy dependencies. Rather than compromise functionality, I analyzed the trade-offs and implemented a split deployment strategy - using Vercel for the React frontend (where serverless excels) and Render for the Python backend (which handles larger dependencies better). This experience taught me when different platform architectures are appropriate and how to make pragmatic engineering decisions.

### Paragraph 4: Business Value
> InvestIQ demonstrates my ability to deliver production-ready applications that balance technical excellence with business considerations. By using free-tier APIs and infrastructure, I minimized costs while maintaining professional quality. The transparent approach to data quality (explicit confidence levels) and graceful error handling shows I understand building for real users, not just demos. You can see the live application at https://invest-iq-wheat.vercel.app.

## For Interviews

### "Walk me through a project you're proud of"
**Answer Script:**

"I'd like to talk about InvestIQ, an AI-enhanced investment research platform I built and deployed to production. The core value proposition is aggregating data from multiple sources - yfinance for market data, NewsAPI for headlines, Reddit for social sentiment, Google Trends for search interest, and the Fear & Greed Index for market sentiment - and using AI to spot patterns and contradictions across these signals.

On the frontend, I used React 18 with TypeScript and shadcn/ui components, which gave me a professional, accessible UI with strong type safety. The backend is Python with FastAPI, chosen for its async capabilities and automatic API documentation.

The most interesting technical challenge was integrating Google Gemini AI. Instead of just basic summarization, I engineered prompts to extract structured insights in three areas: technical pattern recognition where the AI spots divergences in indicators, news sentiment analysis, and what I call cross-signal analysis - where it identifies contradictions like 'technical indicators are bullish but social media mentions spiked 300%, suggesting FOMO'. I implemented smart caching with 1-hour TTL which reduced API costs by 80%.

For deployment, I initially tried putting everything on Vercel but hit their 50MB serverless limit due to pandas and numpy. This taught me an important lesson about when serverless is appropriate versus when you need traditional hosting. I ended up with a split architecture - React on Vercel for instant cold starts, and Python on Render for the heavier data processing. The entire stack auto-deploys from GitHub and costs $0 to run.

What I'm most proud of is not just that it works technically, but that it handles real-world messiness well - graceful degradation when APIs fail, transparent confidence levels so users know data quality, and comprehensive error handling. You can see it live at invest-iq-wheat.vercel.app."

### "Tell me about a time you faced a technical challenge"
**Answer Script:**

"During the deployment of InvestIQ, I hit Vercel's 50MB serverless function limit for Python. My backend uses pandas and numpy for technical analysis calculations, which are large dependencies.

I tried several approaches: first removing unused dependencies like WeasyPrint (30MB), then downgrading pandas and numpy to lighter versions, then restructuring the code to use Mangum as an ASGI adapter. Each attempt taught me more about Vercel's Python runtime limitations.

Eventually I realized I was forcing the wrong architecture. Serverless is excellent for Node.js and lightweight Python functions, but my backend needed a full Python environment with scientific computing libraries. So I pivoted to a split deployment - keeping the React frontend on Vercel (where serverless excels) and moving the backend to Render (which supports larger Python apps).

This challenge taught me two important lessons: first, don't force a tool to do something it wasn't designed for - choose the right platform for each workload. Second, constraints often lead to better architecture. The split deployment is actually more maintainable because each service is optimized for its specific role, and I can scale them independently.

The final architecture costs $0 to run, deploys automatically from GitHub, and performs better than my initial all-in-one approach. It's a good example of how technical challenges can lead to superior solutions if you're willing to reconsider your assumptions."

### "How do you approach integrating AI?"
**Answer Script:**

"I think about AI integration in terms of genuine value-add, not just buzzword compliance. In InvestIQ, I didn't want the AI to just summarize data - I wanted it to spot things that pure mathematical analysis would miss.

I designed three specific AI functions: First, technical pattern recognition where the AI analyzes RSI, moving averages, and volume together to spot divergences. Second, news sentiment analysis that extracts not just positive/negative but key themes and notable events. And third - the most valuable - cross-signal analysis where the AI looks across ALL data sources and identifies contradictions. For example, 'technical indicators show strong momentum, but Reddit mentions spiked 300% in 24 hours, suggesting FOMO rather than fundamental strength.'

I implemented smart caching because the data doesn't change that rapidly - a 1-hour TTL means I can serve repeat requests from cache, reducing API costs by about 80%. I also designed for graceful degradation - if the AI call fails, the report continues with technical and sentiment analysis.

Importantly, I framed everything educationally. The AI 'suggests' rather than 'predicts,' and I'm very clear this is an educational tool, not investment advice. This shows I understand AI's limitations and the importance of responsible implementation.

The prompt engineering was interesting too - I had to be very specific about wanting JSON output with particular fields, and I implemented extraction logic because sometimes Gemini would wrap the JSON in markdown code blocks. Little details like that are what separate a demo from production-ready code."

### "Describe your development process"
**Answer Script:**

"For InvestIQ, I followed a documentation-first approach. Before writing any code, I created CLAUDE.md to capture context, DEV_LOG.md to track decisions, and a comprehensive folder structure. This seems like overhead, but it actually speeds development because you're not making architecture decisions on the fly.

I built the backend first - data collectors, analyzers, and the FastAPI app - because I wanted to validate the data flow before worrying about UI. I used Python type hints throughout and wrote docstrings for every function, which catches errors early and makes the code self-documenting.

For the frontend, I migrated from an initial vanilla JavaScript prototype to React + TypeScript. This added development time up front but paid off in maintainability - TypeScript caught dozens of potential runtime errors during compilation.

I deployed early and often. Rather than perfecting everything locally, I got the basic version deployed to Render and Vercel quickly, then iterated. This exposed issues like the serverless size limit that I wouldn't have caught locally.

Throughout, I documented not just what I built but why. The DEV_LOG tracks challenges, solutions, and learnings. This makes it easy to explain my decisions later and serves as a reference for similar projects.

The result is clean, maintainable code that other developers (or future me) can understand and extend. The comprehensive documentation means someone could pick this up tomorrow and know exactly what's happening and why."

## GitHub Repository Description

**Short:**
```
AI-enhanced investment research platform. React + TypeScript frontend, Python FastAPI backend, Google Gemini AI integration. Deployed on Vercel + Render.
```

**Medium:**
```
🚀 InvestIQ: AI-Enhanced Investment Research Platform

Full-stack application aggregating real-time market data from 5 APIs with Google Gemini AI for pattern recognition and cross-signal analysis.

🔹 React 18 + TypeScript frontend (shadcn/ui)
🔹 Python FastAPI backend with async data fetching
🔹 Google Gemini AI integration with smart caching
🔹 Technical analysis engine (RSI, MAs, volume)
🔹 Deployed on Vercel + Render ($0 cost)

Live Demo: https://invest-iq-wheat.vercel.app
```

## Social Media Posts

### Twitter/X
```
🚀 Just deployed InvestIQ - an AI-enhanced investment research platform!

✅ React + TypeScript frontend
✅ Python FastAPI backend
✅ Google Gemini AI integration
✅ 5 real-time data sources
✅ Production-ready on Vercel + Render

Check it out: https://invest-iq-wheat.vercel.app

#WebDev #AI #Python #React #FullStack
```

### Developer Forums (Reddit, Dev.to, etc.)
```
Title: Built an AI Investment Research Platform - InvestIQ

Hey everyone! I just finished building and deploying InvestIQ, a full-stack investment research platform. Thought I'd share in case anyone's interested in the tech stack or wants to discuss the architecture decisions.

**What it does:**
Aggregates real-time market data from 5 sources (yfinance, NewsAPI, Reddit, Google Trends, Fear & Greed Index), performs technical analysis, and uses Google Gemini AI to spot patterns and contradictions across signals.

**Tech Stack:**
- Frontend: React 18 + TypeScript, Vite, Tailwind CSS, shadcn/ui
- Backend: Python 3.11, FastAPI, async/await
- AI: Google Gemini 2.0 Flash with smart caching
- Deploy: Vercel (frontend) + Render (backend)

**Interesting Challenges:**
1. Hit Vercel's 50MB serverless limit → learned when serverless is appropriate
2. AI response inconsistencies → implemented robust JSON extraction
3. API rate limits → designed graceful degradation

**Performance:**
- Async parallel fetching: 3x speed improvement
- Smart caching: 80% cost reduction
- Total hosting cost: $0

Live demo: https://invest-iq-wheat.vercel.app
GitHub: https://github.com/arjitmat/InvestIQ

Happy to answer questions about the architecture, AI integration, or deployment process!

⚠️ Disclaimer: This is an educational tool, not financial advice.
```

## Email Signature Addition
```
---
Arjit
AI/ML Consultant & Full-Stack Developer

Recent Project: InvestIQ - AI Investment Research Platform
https://invest-iq-wheat.vercel.app
```

## Key Metrics for Discussions

- **Lines of Code:** ~3,500+ (backend) + ~2,000+ (frontend)
- **Development Time:** ~15-20 hours across 3 sessions
- **APIs Integrated:** 5 (yfinance, NewsAPI, Reddit, Google Trends, Fear & Greed)
- **Performance Improvement:** 3x faster with async parallel fetching
- **Cost Reduction:** 80% via smart caching
- **Hosting Cost:** $0/month
- **Deployment Time:** <5 minutes (auto from GitHub)
- **Assets Supported:** 25 (stocks, crypto, indices, commodities)
- **AI Functions:** 3 (technical patterns, news sentiment, cross-signals)
- **Confidence Levels:** 4 (HIGH, MEDIUM, LOW, CONTEXT)

## Tags for Job Applications

**Technical Skills:**
React, TypeScript, Python, FastAPI, AI Integration, Google Gemini, API Integration, Async Programming, Full-Stack Development, Web Development, Frontend Development, Backend Development, DevOps, CI/CD, Vercel, Render, Git, GitHub

**Soft Skills:**
Problem Solving, Architecture Design, Technical Documentation, Production Deployment, Cost Optimization, Performance Optimization, Error Handling, User-Focused Design

**Domain Knowledge:**
Financial Technology (FinTech), Investment Research, Technical Analysis, Sentiment Analysis, Data Aggregation, AI/ML Applications
