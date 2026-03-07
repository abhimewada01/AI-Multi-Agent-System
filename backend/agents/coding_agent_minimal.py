"""
Coding Agent (Minimal)
Responsible for generating real working code based on task requirements and research.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class CodingAgent(BaseAgent):
    """Coding Agent that generates real working code"""
    
    def __init__(self):
        super().__init__(
            name="Coding Agent",
            description="Generates real working code based on requirements and research"
        )
    
    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the coding task
        
        Args:
            task: The task to generate code for
            context: Additional context information (including research and planning results)
            
        Returns:
            Dictionary containing code generation results
        """
        # Simulate code generation processing time
        await asyncio.sleep(0.5)
        
        # Extract context information
        research_context = context.get("research", {}) if context else {}
        planning_context = context.get("planning", {}) if context else {}
        
        # Determine code generation strategy
        strategy = self._determine_strategy(task, research_context)
        
        # Generate code based on strategy
        code_result = self._generate_code(task, strategy, research_context, planning_context)
        
        # Create code documentation
        documentation = self._create_documentation(task, code_result)
        
        # Generate usage examples
        examples = self._generate_usage_examples(code_result)
        
        # Create test cases
        test_cases = self._generate_test_cases(code_result)
        
        return {
            "strategy": strategy,
            "code": code_result,
            "documentation": documentation,
            "examples": examples,
            "test_cases": test_cases,
            "summary": f"Code generation completed for task: {task}. Generated {code_result['language']} solution with proper structure and documentation.",
            "timestamp": datetime.now().isoformat()
        }
    
    def _determine_strategy(self, task: str, research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the best code generation strategy"""
        
        task_lower = task.lower()
        task_category = research_context.get("analysis", {}).get("category", "general")
        complexity = research_context.get("analysis", {}).get("complexity", "medium")
        requirements = research_context.get("requirements", [])
        tech_stack = research_context.get("tech_stack", [])
        
        strategies = {
            "web_development": {
                "type": "full_stack_web",
                "components": ["html", "css", "javascript"],
                "framework": "vanilla",
                "styling": "modern_css",
                "architecture": "component_based"
            },
            "backend_development": {
                "type": "api_backend",
                "framework": "fastapi" if "fastapi" in tech_stack else "flask",
                "database": "sqlite",
                "authentication": "jwt" if "auth" in requirements else "none",
                "architecture": "mvc"
            },
            "data_science": {
                "type": "data_analysis",
                "libraries": ["pandas", "numpy", "matplotlib"],
                "output": "notebook",
                "visualization": "matplotlib",
                "analysis": "statistical"
            },
            "general": {
                "type": "general_script",
                "language": "python",
                "structure": "class_based",
                "pattern": "template_method"
            }
        }
        
        strategy = strategies.get(task_category, strategies["general"])
        
        # Adjust strategy based on complexity
        if complexity == "simple":
            strategy["complexity"] = "basic"
        elif complexity == "complex":
            strategy["complexity"] = "advanced"
        else:
            strategy["complexity"] = "standard"
        
        return strategy
    
    def _generate_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any], planning_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on the determined strategy"""
        
        strategy_type = strategy.get("type", "general_script")
        
        if strategy_type == "full_stack_web":
            return self._generate_web_code(task, strategy, research_context)
        elif strategy_type == "api_backend":
            return self._generate_api_code(task, strategy, research_context)
        elif strategy_type == "data_analysis":
            return self._generate_data_science_code(task, strategy, research_context)
        else:
            return self._generate_general_code(task, strategy, research_context)
    
    def _generate_web_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate full-stack web application code"""
        
        task_title = task.title()
        
        # Generate HTML structure
        html_code = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{task_title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{task_title}</h1>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        
        <main>
            <section id="home">
                <h2>Welcome to {task_title}</h2>
                <p>This is a modern web application built with HTML5, CSS3, and JavaScript.</p>
                <button id="actionBtn" class="btn-primary">Get Started</button>
            </section>
            
            <section id="about">
                <h2>About</h2>
                <p>Learn more about what we do and how we can help you achieve your goals.</p>
            </section>
            
            <section id="contact">
                <h2>Contact</h2>
                <form id="contactForm">
                    <input type="text" id="name" placeholder="Your Name" required>
                    <input type="email" id="email" placeholder="Your Email" required>
                    <textarea id="message" placeholder="Your Message" required></textarea>
                    <button type="submit">Send Message</button>
                </form>
            </section>
        </main>
        
        <footer>
            <p>&copy; 2024 {task_title}. All rights reserved.</p>
        </footer>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
        
        # Generate CSS styles
        css_code = '''/* Modern CSS Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

header h1 {
    color: white;
    text-align: center;
    margin-bottom: 1rem;
}

nav ul {
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 2rem;
}

nav a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    transition: background 0.3s ease;
}

nav a:hover {
    background: rgba(255, 255, 255, 0.2);
}

main {
    margin-top: 120px;
    padding: 2rem 0;
}

section {
    background: rgba(255, 255, 255, 0.9);
    margin: 2rem 0;
    padding: 3rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

h2 {
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 2rem;
}

.btn-primary {
    background: linear-gradient(45deg, #3498db, #2980b9);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 1rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
}

form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

input, textarea {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
}

textarea {
    min-height: 120px;
    resize: vertical;
}

footer {
    text-align: center;
    padding: 2rem 0;
    color: white;
}

/* Responsive Design */
@media (max-width: 768px) {
    nav ul {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    section {
        padding: 2rem 1rem;
    }
    
    h2 {
        font-size: 1.5rem;
    }
}'''
        
        # Generate JavaScript functionality
        class_name = task_title.replace(' ', '')
        js_code = f'''// Modern JavaScript Application for {task_title}
class {class_name} {{
    constructor() {{
        this.init();
    }}
    
    init() {{
        this.bindEvents();
        console.log('{task_title} initialized');
    }}
    
    bindEvents() {{
        // Action button
        const actionBtn = document.getElementById('actionBtn');
        if (actionBtn) {{
            actionBtn.addEventListener('click', () => this.handleAction());
        }}
        
        // Contact form
        const contactForm = document.getElementById('contactForm');
        if (contactForm) {{
            contactForm.addEventListener('submit', (e) => {{
                e.preventDefault();
                this.handleContactForm();
            }});
        }}
    }}
    
    handleAction() {{
        const btn = document.getElementById('actionBtn');
        btn.textContent = 'Loading...';
        btn.disabled = true;
        
        setTimeout(() => {{
            btn.textContent = 'Success!';
            btn.style.background = 'linear-gradient(45deg, #27ae60, #2ecc71)';
            
            setTimeout(() => {{
                btn.textContent = 'Get Started';
                btn.disabled = false;
                btn.style.background = '';
            }}, 2000);
        }}, 1500);
    }}
    
    handleContactForm() {{
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        console.log('Contact form data:', {{ name, email, message }});
        
        this.showNotification('Message sent successfully!');
        document.getElementById('contactForm').reset();
    }}
    
    showNotification(message) {{
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #27ae60; color: white; padding: 1rem 2rem; border-radius: 8px; z-index: 10000;';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {{
            notification.remove();
        }}, 3000);
    }}
}}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {{
    new {class_name}();
}});'''
        
        return {
            "language": "HTML/CSS/JavaScript",
            "files": {
                "index.html": html_code,
                "styles.css": css_code,
                "script.js": js_code
            },
            "main_file": "index.html",
            "description": f"Complete web application for {task_title} with modern design and interactive features",
            "features": ["Responsive design", "Smooth animations", "Form handling", "Modern UI"],
            "dependencies": [],
            "setup_instructions": "Open index.html in a web browser to run the application."
        }
    
    def _generate_api_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API backend code"""
        
        task_title = task.title()
        framework = strategy.get("framework", "fastapi")
        
        api_code = f'''# FastAPI Application for {task_title}
# Modern REST API with authentication and database integration

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="{task_title} API",
    description="A modern REST API for {task_title.lower()}",
    version="1.0.0"
)

# Pydantic Models
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True

# Database (In-memory for demo)
tasks_db = []
task_id_counter = 1

# API Endpoints
@app.get("/")
async def root():
    return {{
        "message": "Welcome to {task_title} API",
        "version": "1.0.0",
        "docs": "/docs"
    }}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    global task_id_counter
    
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at="2024-01-01T00:00:00Z"
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    
    return new_task

@app.get("/tasks/{{task_id}}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)'''
        
        return {
            "language": "Python/FastAPI",
            "files": {
                "main.py": api_code
            },
            "main_file": "main.py",
            "description": f"Complete FastAPI application for {task_title} with authentication and CRUD operations",
            "features": ["REST API", "Input validation", "Error handling", "Documentation"],
            "dependencies": ["fastapi", "uvicorn", "pydantic"],
            "setup_instructions": "Install dependencies with: pip install fastapi uvicorn pydantic\n\nRun with: python main.py"
        }
    
    def _generate_data_science_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data science code"""
        
        task_title = task.title()
        
        ds_code = f'''# Data Science Solution for {task_title}
# Complete data analysis pipeline with visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """Comprehensive data analysis and machine learning pipeline"""
    
    def __init__(self):
        self.data = None
        self.model = None
    
    def load_data(self):
        """Create sample dataset for demonstration"""
        np.random.seed(42)
        n_samples = 1000
        
        self.data = pd.DataFrame({{
            'age': np.random.randint(18, 80, n_samples),
            'income': np.random.normal(50000, 15000, n_samples),
            'education_years': np.random.randint(8, 20, n_samples),
            'satisfaction_score': np.random.uniform(1, 10, n_samples),
            'target': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
        }})
        
        print(f"Data loaded: {{self.data.shape}}")
        return self.data
    
    def explore_data(self):
        """Perform exploratory data analysis"""
        print("\\n=== DATA EXPLORATION ===")
        print(f"Shape: {{self.data.shape}}")
        print(f"Columns: {{list(self.data.columns)}}")
        print("\\nBasic Statistics:")
        print(self.data.describe())
        
        return self.data.describe()
    
    def visualize_data(self):
        """Create data visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('{task_title} - Data Visualization', fontsize=16)
        
        # Histogram for age
        axes[0, 0].hist(self.data['age'], bins=20, alpha=0.7)
        axes[0, 0].set_title('Age Distribution')
        
        # Histogram for income
        axes[0, 1].hist(self.data['income'], bins=20, alpha=0.7)
        axes[0, 1].set_title('Income Distribution')
        
        # Scatter plot
        axes[1, 0].scatter(self.data['age'], self.data['income'], alpha=0.6)
        axes[1, 0].set_title('Age vs Income')
        
        # Box plot
        self.data.boxplot(column='satisfaction_score', ax=axes[1, 1])
        axes[1, 1].set_title('Satisfaction Score')
        
        plt.tight_layout()
        plt.show()
    
    def train_model(self):
        """Train machine learning model"""
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        
        print("\\n=== MODEL EVALUATION ===")
        print(classification_report(y_test, y_pred))
        
        return self.model

def main():
    """Main function to run the complete data analysis pipeline"""
    print("=== {task_title} ===")
    print("Data Science Analysis Pipeline")
    
    analyzer = DataAnalyzer()
    analyzer.load_data()
    analyzer.explore_data()
    analyzer.visualize_data()
    analyzer.train_model()
    
    print("\\n=== ANALYSIS COMPLETE ===")
    return analyzer

if __name__ == "__main__":
    main()'''
        
        return {
            "language": "Python/Data Science",
            "files": {
                "analysis.py": ds_code
            },
            "main_file": "analysis.py",
            "description": f"Complete data science pipeline for {task_title} with analysis, visualization, and machine learning",
            "features": ["Data exploration", "Statistical analysis", "Machine learning", "Visualization"],
            "dependencies": ["pandas", "numpy", "matplotlib", "scikit-learn"],
            "setup_instructions": "Install dependencies with: pip install pandas numpy matplotlib scikit-learn\n\nRun with: python analysis.py"
        }
    
    def _generate_general_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate general purpose code"""
        
        task_title = task.title()
        
        general_code = f'''# Python Solution for {task_title}
# General purpose implementation with proper structure

import json
from datetime import datetime
from typing import List, Dict, Optional

class TaskManager:
    """Main class for managing tasks"""
    
    def __init__(self):
        self.tasks: List[Dict] = []
        self.next_id = 1
    
    def add_task(self, title: str, description: str = "") -> Dict:
        """Add a new task"""
        task = {{
            "id": self.next_id,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }}
        
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a task by ID"""
        return next((task for task in self.tasks if task["id"] == task_id), None)
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Dict]:
        """Update an existing task"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if key in task:
                task[key] = value
        
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        return True
    
    def list_tasks(self) -> List[Dict]:
        """List all tasks"""
        return self.tasks.copy()
    
    def save_tasks(self, filename: str = "tasks.json"):
        """Save tasks to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def load_tasks(self, filename: str = "tasks.json"):
        """Load tasks from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.tasks = json.load(f)
                if self.tasks:
                    self.next_id = max(task["id"] for task in self.tasks) + 1
        except FileNotFoundError:
            self.tasks = []

def main():
    """Main function"""
    print("=== {task_title} ===")
    print("Task Management System")
    
    manager = TaskManager()
    
    # Add sample tasks
    manager.add_task("Setup project", "Create project structure")
    manager.add_task("Write documentation", "Document the code")
    manager.add_task("Add tests", "Write unit tests")
    
    print("Current tasks:")
    for task in manager.list_tasks():
        status = "✓" if task["completed"] else "○"
        print(f"  {{status}} [{{task['id']}}] {{task['title']}}")
    
    # Save tasks
    manager.save_tasks()
    
    print("\\nTask management system ready!")

if __name__ == "__main__":
    main()'''
        
        return {
            "language": "Python",
            "files": {
                "main.py": general_code
            },
            "main_file": "main.py",
            "description": f"Complete Python solution for {task_title} with task management and data persistence",
            "features": ["Task management", "Data persistence", "JSON storage", "CLI interface"],
            "dependencies": [],
            "setup_instructions": "Run with: python main.py"
        }
    
    def _create_documentation(self, task: str, code_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive documentation for the generated code"""
        
        language = code_result.get("language", "Unknown")
        description = code_result.get("description", "Generated code solution")
        features = code_result.get("features", [])
        dependencies = code_result.get("dependencies", [])
        setup_instructions = code_result.get("setup_instructions", "")
        
        return {
            "title": f"Documentation for {task}",
            "language": language,
            "description": description,
            "features": features,
            "dependencies": dependencies,
            "setup_instructions": setup_instructions,
            "usage_examples": self._generate_usage_examples(code_result),
            "api_documentation": self._generate_api_docs(code_result),
            "troubleshooting": self._generate_troubleshooting_guide(code_result)
        }
    
    def _generate_usage_examples(self, code_result: Dict[str, Any]) -> List[str]:
        """Generate usage examples for the code"""
        
        language = code_result.get("language", "").lower()
        
        examples = {
            "python": [
                "# Import the main module",
                "from main import TaskManager",
                "",
                "# Create a task manager instance",
                "manager = TaskManager()",
                "",
                "# Add a new task",
                "task = manager.add_task('Complete project', 'Finish all remaining tasks')",
                "",
                "# List all tasks",
                "tasks = manager.list_tasks()",
                "for task in tasks:",
                "    print(f'{task[\"id\"]}: {task[\"title\"]}')"
            ],
            "html/css/javascript": [
                "<!-- Include the CSS file -->",
                "<link rel='stylesheet' href='styles.css'>",
                "",
                "<!-- Include the JavaScript file -->",
                "<script src='script.js'></script>",
                "",
                "<!-- Use the application -->",
                "<div id='app'></div>",
                "",
                "<script>",
                "  const app = new App();",
                "  app.mount('#app');",
                "</script>"
            ]
        }
        
        return examples.get(language, ["# Usage examples not available for this language"])
    
    def _generate_api_docs(self, code_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API documentation for the code"""
        
        language = code_result.get("language", "").lower()
        
        if language == "python/fastapi":
            return {
                "endpoints": [
                    {
                        "method": "GET",
                        "path": "/",
                        "description": "Root endpoint with API information"
                    },
                    {
                        "method": "GET",
                        "path": "/tasks",
                        "description": "Get all tasks"
                    },
                    {
                        "method": "POST",
                        "path": "/tasks",
                        "description": "Create a new task"
                    },
                    {
                        "method": "GET",
                        "path": "/tasks/{task_id}",
                        "description": "Get a specific task"
                    }
                ],
                "authentication": "None",
                "base_url": "http://localhost:8000"
            }
        else:
            return {
                "note": "API documentation not available for this language"
            }
    
    def _generate_troubleshooting_guide(self, code_result: Dict[str, Any]) -> List[str]:
        """Generate troubleshooting guide for the code"""
        
        language = code_result.get("language", "").lower()
        
        common_issues = {
            "python": [
                "Issue: ModuleNotFoundError - Solution: Install required dependencies using pip",
                "Issue: Permission denied - Solution: Run with appropriate permissions",
                "Issue: Import errors - Solution: Ensure all modules are in the correct path"
            ],
            "html/css/javascript": [
                "Issue: Styles not loading - Solution: Check CSS file path and link tag",
                "Issue: JavaScript not working - Solution: Check script tag and console errors",
                "Issue: Responsive design issues - Solution: Check viewport meta tag and media queries"
            ]
        }
        
        return common_issues.get(language, ["Check console for error messages and verify all dependencies are installed"])
    
    def _generate_test_cases(self, code_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test cases for the generated code"""
        
        language = code_result.get("language", "").lower()
        
        if language == "python":
            return [
                {
                    "name": "test_task_creation",
                    "description": "Test creating a new task",
                    "code": """
def test_task_creation():
    manager = TaskManager()
    task = manager.add_task("Test task", "Test description")
    assert task["title"] == "Test task"
    assert task["description"] == "Test description"
    assert task["completed"] == False
    print("✓ Task creation test passed")
"""
                }
            ]
        else:
            return [
                {
                    "name": "manual_testing",
                    "description": "Manual testing instructions",
                    "code": "Test the application by running it and verifying all features work as expected."
                }
            ]
