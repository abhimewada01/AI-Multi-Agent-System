# AI Multi-Agent System

A sophisticated AI system where multiple intelligent agents collaborate to solve complex tasks through research, planning, coding, and execution.

## 🚀 Overview

The AI Multi-Agent System is an advanced platform that orchestrates four specialized AI agents to work together on complex tasks. Each agent has a specific role and expertise, creating a comprehensive workflow that transforms user requests into detailed, actionable solutions.

## 🏗️ System Architecture

```
User Input → Research Agent → Planning Agent → Coding Agent → Execution Agent → Final Result
```

### Agent Workflow

1. **Research Agent**: Gathers and analyzes information about the task
2. **Planning Agent**: Creates detailed step-by-step execution plans
3. **Coding Agent**: Generates technical solutions and code implementations
4. **Execution Agent**: Synthesizes all results into comprehensive final outputs

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **FastAPI** - Modern, fast web framework for APIs
- **LangChain** - Framework for building AI applications
- **OpenAI API** - Large language model interface

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables and flexbox/grid
- **JavaScript ES6+** - Modern frontend functionality
- **Font Awesome** - Icon library

### Infrastructure
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation and settings management
- **AsyncIO** - Asynchronous programming support

## 📁 Project Structure

```
AI-Multi-Agent-System/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── agents/
│   │   ├── research_agent.py   # Research and information gathering
│   │   ├── planning_agent.py   # Task planning and breakdown
│   │   ├── coding_agent.py     # Code generation and technical solutions
│   │   └── execution_agent.py  # Result synthesis and coordination
│   └── utils/
│       └── llm_helper.py       # LLM interface and utilities
├── frontend/
│   ├── index.html              # Main web interface
│   ├── style.css               # Modern responsive styling
│   └── script.js               # Frontend functionality
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Agent Collaboration**: Four specialized AI agents working in sequence
- **Real-time Progress Tracking**: Visual progress indicators for each agent
- **Comprehensive Results**: Detailed outputs from each processing phase
- **Modern Web Interface**: Clean, responsive, and user-friendly UI
- **Error Handling**: Robust error handling and user feedback

### 🎨 User Interface
- **Clean Dashboard**: Modern, intuitive interface design
- **Progress Visualization**: Real-time agent status and progress bars
- **Tabbed Results**: Organized display of research, planning, code, and final results
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Interactive Elements**: Copy code, switch tabs, view detailed information

### 🔧 Technical Features
- **Asynchronous Processing**: Non-blocking agent execution
- **Structured Outputs**: JSON-based data flow between agents
- **Quality Scoring**: Automated quality assessment for each phase
- **Modular Architecture**: Clean separation of concerns
- **Extensible Design**: Easy to add new agents or modify existing ones

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git (for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Multi-Agent-System
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```
   
   Replace `your_openai_api_key_here` with your actual OpenAI API key.

5. **Run the application**
   ```bash
   cd backend
   python main.py
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Web Interface: http://localhost:8000/static/index.html
   - API Documentation: http://localhost:8000/docs

## 📖 Usage Guide

### Basic Usage

1. **Open the web interface** at `http://localhost:8000/static/index.html`
2. **Enter your task** in the input field. Examples:
   - "Build a simple Python REST API for user management"
   - "Explain machine learning with code examples"
   - "Create a web scraping script for data collection"
   - "Design a database schema for an e-commerce platform"

3. **Click "Start Processing"** to begin the multi-agent workflow

4. **Monitor progress** as each agent completes its work:
   - Research Agent gathers information
   - Planning Agent creates execution plan
   - Coding Agent generates solutions
   - Execution Agent synthesizes final results

5. **Explore results** using the tabbed interface:
   - **Summary**: Overview of all results
   - **Research**: Detailed research findings
   - **Planning**: Execution plan and steps
   - **Code**: Generated code and technical solutions
   - **Final Output**: Comprehensive final result

### Advanced Features

#### API Usage
You can also interact with the system directly via API:

```python
import requests

# Process a task via API
response = requests.post('http://localhost:8000/process', json={
    'task': 'Build a simple Python API',
    'context': 'For learning purposes'
})

result = response.json()
print(result['final_output'])
```

#### Individual Agent Testing
Test individual agents:

```python
# Research only
response = requests.post('http://localhost:8000/agent/research', json={
    'task': 'Explain quantum computing'
})

# Planning only
response = requests.post('http://localhost:8000/agent/plan', json={
    'task': 'Create a mobile app'
})
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
# Optional: Custom model settings
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
```

### Customization
You can customize agent behavior by modifying the system prompts in `backend/utils/llm_helper.py` or individual agent files.

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run specific agent tests
pytest backend/agents/test_research_agent.py
```

### Manual Testing
Use the provided test functions in each agent file:

```bash
cd backend/agents
python research_agent.py
python planning_agent.py
python coding_agent.py
python execution_agent.py
```

## 📊 API Endpoints

### Main Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /process` - Process task through all agents
- `GET /agents/status` - Get agent statuses

### Individual Agent Endpoints
- `POST /agent/research` - Run research agent only
- `POST /agent/plan` - Run planning agent only

### Response Format
```json
{
  "task": "original task",
  "research_result": {...},
  "planning_result": {...},
  "coding_result": {...},
  "execution_result": {...},
  "final_output": "comprehensive result",
  "total_time": 123.45
}
```

## 🎯 Example Tasks

### Software Development
- "Build a simple Python REST API for user management"
- "Create a React todo app with backend integration"
- "Design a microservices architecture for e-commerce"

### Data Science
- "Explain machine learning with practical code examples"
- "Create a data analysis script for sales data"
- "Build a recommendation system algorithm"

### Research & Analysis
- "Research the latest trends in AI technology"
- "Analyze market opportunities for renewable energy"
- "Create a competitive analysis report"

### Educational
- "Explain quantum computing in simple terms"
- "Create a tutorial on blockchain technology"
- "Design a curriculum for web development"

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Check that the API key has sufficient credits
   - Verify the API key is not expired

2. **Connection Errors**
   - Check if the backend server is running on port 8000
   - Verify firewall settings aren't blocking the connection
   - Try accessing `http://localhost:8000/health` to test connectivity

3. **Slow Response Times**
   - OpenAI API response times can vary
   - Consider using a faster model like `gpt-3.5-turbo`
   - Check your internet connection

4. **Memory Issues**
   - Large tasks may require significant memory
   - Consider breaking down complex tasks
   - Monitor system resources during processing

### Debug Mode
Enable debug logging by setting:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 🚀 Future Enhancements

### Planned Features
- [ ] **Additional Agents**: Testing, Documentation, Deployment agents
- [ ] **Custom Workflows**: User-defined agent sequences
- [ ] **Batch Processing**: Process multiple tasks simultaneously
- [ ] **Result History**: Save and retrieve previous results
- [ ] **Export Options**: Download results as PDF, Word, or Markdown
- [ ] **Agent Templates**: Pre-configured agent behaviors
- [ ] **Real-time Collaboration**: Multi-user support
- [ ] **Advanced Analytics**: Performance metrics and insights

### Technical Improvements
- [ ] **Caching**: Redis-based result caching
- [ ] **Database**: PostgreSQL for persistent storage
- [ ] **Message Queue**: Celery for background processing
- [ ] **Monitoring**: Prometheus metrics and Grafana dashboards
- [ ] **Load Balancing**: Multiple backend instances
- [ ] **Security**: Authentication and authorization

### AI Enhancements
- [ ] **Multiple LLM Providers**: Support for Claude, Gemini, etc.
- [ ] **Fine-tuning**: Custom models for specific domains
- [ ] **Context Memory**: Better conversation context handling
- [ ] **Tool Integration**: Code execution, web browsing capabilities

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** following the existing code style
4. **Add tests** for new functionality
5. **Run tests**: `pytest`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Code Style
- Use Black for code formatting: `black .`
- Follow PEP 8 guidelines
- Add type hints where appropriate
- Include docstrings for functions and classes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing powerful language models
- **LangChain** for the excellent AI framework
- **FastAPI** for the modern web framework
- **Font Awesome** for the icon library

## 📞 Support

For support, please:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the API documentation at `/docs`

## 🌟 Show Your Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting improvements
- 📝 Contributing to the codebase

---

**Built with ❤️ by the AI Multi-Agent System Team**
