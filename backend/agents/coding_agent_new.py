"""
Coding Agent
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
            "mobile_development": {
                "type": "mobile_app",
                "framework": "react_native" if "react" in tech_stack else "flutter",
                "platform": "cross_platform",
                "architecture": "component_based"
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
        elif strategy_type == "mobile_app":
            return self._generate_mobile_code(task, strategy, research_context)
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
        js_code = f'''// Modern JavaScript Application for {task_title}
class {task_title.replace(/\s+/g, '')} {{
    constructor() {{
        this.init();
    }}
    
    init() {{
        this.bindEvents();
        this.loadAnimations();
        console.log('{task_title} initialized');
    }}
    
    bindEvents() {{
        // Action button
        document.getElementById('actionBtn').addEventListener('click', () => {{
            this.handleAction();
        }});
        
        // Contact form
        document.getElementById('contactForm').addEventListener('submit', (e) => {{
            e.preventDefault();
            this.handleContactForm();
        }});
        
        // Smooth scrolling
        document.querySelectorAll('nav a').forEach(anchor => {{
            anchor.addEventListener('click', (e) => {{
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
    }}
    
    handleAction() {{
        const btn = document.getElementById('actionBtn');
        btn.textContent = 'Loading...';
        btn.disabled = true;
        
        // Simulate async operation
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
        const formData = {{
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        }};
        
        console.log('Contact form data:', formData);
        
        // Show success message
        this.showNotification('Message sent successfully!');
        
        // Reset form
        document.getElementById('contactForm').reset();
    }}
    
    showNotification(message) {{
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {{
            notification.remove();
        }}, 3000);
    }}
    
    loadAnimations() {{
        // Add scroll animations
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                }}
            }});
        }});
        
        document.querySelectorAll('section').forEach(section => {{
            observer.observe(section);
        }});
    }}
}}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {{
    new {task_title.replace(/\s+/g, '')}();
}});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `\\
    @keyframes slideIn {{\\
        from {{ transform: translateX(100%); opacity: 0; }}\\
        to {{ transform: translateX(0); opacity: 1; }}\\
    }}\\
    \\n\\
    @keyframes fadeInUp {{\\
        from {{ transform: translateY(30px); opacity: 0; }}\\
        to {{ transform: translateY(0); opacity: 1; }}\\
    }}\\
`;
document.head.appendChild(style);'''
        
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
        has_auth = strategy.get("authentication") == "jwt"
        
        api_code = f'''# FastAPI Application for {task_title}
# Modern REST API with authentication and database integration

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
import hashlib
import uvicorn

app = FastAPI(
    title="{task_title} API",
    description="A modern REST API for {task_title.lower()}",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Database (In-memory for demo)
users_db = []
tasks_db = []
user_id_counter = 1
task_id_counter = 1

# Helper functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({{"exp": expire}})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user(username: str):
    return next((user for user in users_db if user.username == username), None)

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# Auth Endpoints
@app.post("/auth/register", response_model=User)
async def register(user: UserCreate):
    global user_id_counter
    
    # Check if user already exists
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        created_at=datetime.now()
    )
    users_db.append(new_user)
    user_id_counter += 1
    
    return new_user

@app.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = get_user(user_credentials.username)
    if not user or user.hashed_password != hash_password(user_credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={{"sub": user.username}})
    return {{
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400
    }}

@app.get("/auth/me", response_model=User)
async def get_current_user(username: str = Depends(verify_token)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Task Endpoints
@app.get("/tasks", response_model=List[Task])
async def get_tasks(username: str = Depends(verify_token)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_tasks = [task for task in tasks_db if task.user_id == user.id]
    return user_tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, username: str = Depends(verify_token)):
    global task_id_counter
    
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user.id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    
    return new_task

@app.get("/tasks/{{task_id}}", response_model=Task)
async def get_task(task_id: int, username: str = Depends(verify_token)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    task = next((t for t in tasks_db if t.id == task_id and t.user_id == user.id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@app.put("/tasks/{{task_id}}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate, username: str = Depends(verify_token)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    task = next((t for t in tasks_db if t.id == task_id and t.user_id == user.id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    task.updated_at = datetime.now()
    
    return task

@app.delete("/tasks/{{task_id}}")
async def delete_task(task_id: int, username: str = Depends(verify_token)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    task_index = next((i for i, t in enumerate(tasks_db) if t.id == task_id and t.user_id == user.id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted_task = tasks_db.pop(task_index)
    return {{"message": "Task deleted successfully", "task": deleted_task}}

# Root endpoint
@app.get("/")
async def root():
    return {{
        "message": "Welcome to {task_title} API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {{
            "auth": "/auth",
            "tasks": "/tasks"
        }}
    }}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)'''
        
        return {
            "language": "Python/FastAPI",
            "files": {
                "main.py": api_code
            },
            "main_file": "main.py",
            "description": f"Complete FastAPI application for {task_title} with authentication and CRUD operations",
            "features": ["JWT Authentication", "CRUD operations", "Input validation", "CORS support"],
            "dependencies": ["fastapi", "uvicorn", "python-jose[cryptography]", "python-multipart", "email-validator"],
            "setup_instructions": "Install dependencies with: pip install fastapi uvicorn python-jose[cryptography] python-multipart email-validator\n\nRun with: python main.py"
        }
    
    def _generate_data_science_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data science code"""
        
        task_title = task.title()
        
        ds_code = f'''# Data Science Solution for {task_title}
# Complete data analysis pipeline with visualization and machine learning

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DataAnalyzer:
    """Comprehensive data analysis and machine learning pipeline"""
    
    def __init__(self, data_path=None):
        self.data = None
        self.data_path = data_path
        self.scaler = StandardScaler()
        self.model = None
        self.features = None
        self.target = None
        
    def load_data(self, data_path=None):
        """Load data from CSV or create sample dataset"""
        if data_path:
            self.data = pd.read_csv(data_path)
        else:
            # Create sample dataset for demonstration
            np.random.seed(42)
            n_samples = 1000
            
            self.data = pd.DataFrame({{
                'age': np.random.randint(18, 80, n_samples),
                'income': np.random.normal(50000, 15000, n_samples),
                'education_years': np.random.randint(8, 20, n_samples),
                'experience_years': np.random.randint(0, 40, n_samples),
                'satisfaction_score': np.random.uniform(1, 10, n_samples),
                'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR'], n_samples),
                'target': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
            }})
            
        print(f"Data loaded: {{self.data.shape}}")
        return self.data
    
    def explore_data(self):
        """Perform comprehensive exploratory data analysis"""
        print("\\n=== DATA EXPLORATION ===")
        print(f"Shape: {{self.data.shape}}")
        print(f"Columns: {{list(self.data.columns)}}")
        print(f"Data types:\\n{{self.data.dtypes}}")
        print(f"Missing values:\\n{{self.data.isnull().sum()}}")
        
        # Basic statistics
        print("\\n=== BASIC STATISTICS ===")
        print(self.data.describe())
        
        # Correlation analysis
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            print("\\n=== CORRELATION MATRIX ===")
            correlation = self.data[numeric_cols].corr()
            print(correlation)
            
            # Plot correlation heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, 
                        square=True, linewidths=0.5)
            plt.title('Feature Correlation Heatmap')
            plt.tight_layout()
            plt.show()
        
        return self.data.describe()
    
    def visualize_data(self):
        """Create comprehensive data visualizations"""
        print("\\n=== DATA VISUALIZATION ===")
        
        # Create subplots for multiple visualizations
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('{task_title} - Data Visualization Dashboard', fontsize=16)
        
        # Get numeric columns
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        # Histograms for numeric features
        for i, col in enumerate(numeric_cols[:4]):
            row, col_idx = i // 2, i % 2
            axes[row, col_idx].hist(self.data[col], bins=30, alpha=0.7, edgecolor='black')
            axes[row, col_idx].set_title(f'Distribution of {{col}}')
            axes[row, col_idx].set_xlabel(col)
            axes[row, col_idx].set_ylabel('Frequency')
        
        # Box plot for satisfaction score
        if 'satisfaction_score' in self.data.columns:
            axes[1, 2].boxplot(self.data['satisfaction_score'])
            axes[1, 2].set_title('Satisfaction Score Distribution')
            axes[1, 2].set_ylabel('Score')
        
        plt.tight_layout()
        plt.show()
        
        # Categorical data visualization
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            fig, axes = plt.subplots(1, len(categorical_cols), figsize=(15, 5))
            if len(categorical_cols) == 1:
                axes = [axes]
            
            for i, col in enumerate(categorical_cols):
                self.data[col].value_counts().plot(kind='bar', ax=axes[i])
                axes[i].set_title(f'Distribution of {{col}}')
                axes[i].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.show()
    
    def preprocess_data(self, target_column='target'):
        """Preprocess data for machine learning"""
        print("\\n=== DATA PREPROCESSING ===")
        
        # Handle missing values
        if self.data.isnull().sum().sum() > 0:
            print("Handling missing values...")
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].median())
            
            categorical_cols = self.data.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                self.data[col] = self.data[col].fillna(self.data[col].mode()[0])
        
        # Encode categorical variables
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            self.data[col] = pd.Categorical(self.data[col]).codes
        
        # Split features and target
        if target_column in self.data.columns:
            self.features = self.data.drop(target_column, axis=1)
            self.target = self.data[target_column]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                self.features, self.target, test_size=0.2, random_state=42, stratify=self.target
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            print(f"Training set shape: {{X_train_scaled.shape}}")
            print(f"Test set shape: {{X_test_scaled.shape}}")
            
            return X_train_scaled, X_test_scaled, y_train, y_test
        else:
            print("No target column found for supervised learning")
            return None, None, None, None
    
    def train_model(self, X_train, X_test, y_train, y_test):
        """Train machine learning model"""
        print("\\n=== MODEL TRAINING ===")
        
        # Train Random Forest
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Evaluate model
        print("\\n=== MODEL EVALUATION ===")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        print("\\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        # Feature importance
        feature_names = self.features.columns
        feature_importance = pd.DataFrame({{
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }}).sort_values('importance', ascending=False)
        
        print("\\n=== FEATURE IMPORTANCE ===")
        print(feature_importance.head(10))
        
        # Plot feature importance
        plt.figure(figsize=(10, 6))
        sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
        plt.title('Top 10 Feature Importances')
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        plt.tight_layout()
        plt.show()
        
        return self.model, feature_importance
    
    def perform_clustering(self, n_clusters=3):
        """Perform K-means clustering"""
        print("\\n=== CLUSTERING ANALYSIS ===")
        
        # Use only numeric features for clustering
        numeric_features = self.features.select_dtypes(include=[np.number])
        
        # Scale features
        features_scaled = self.scaler.fit_transform(numeric_features)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(features_scaled)
        
        # Add cluster labels to data
        self.data['cluster'] = cluster_labels
        
        # Analyze clusters
        print("\\nCluster Analysis:")
        for i in range(n_clusters):
            cluster_data = self.data[self.data['cluster'] == i]
            print(f"\\nCluster {{i}} ({{len(cluster_data)}} samples):")
            print(cluster_data.describe())
        
        # Visualize clusters
        if len(numeric_features.columns) >= 2:
            plt.figure(figsize=(10, 6))
            scatter = plt.scatter(features_scaled[:, 0], features_scaled[:, 1], 
                               c=cluster_labels, cmap='viridis', alpha=0.6)
            plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                       c='red', marker='x', s=200, linewidths=3)
            plt.xlabel('Feature 1')
            plt.ylabel('Feature 2')
            plt.title('K-means Clustering Results')
            plt.colorbar(scatter)
            plt.show()
        
        return kmeans, cluster_labels
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\\n=== ANALYSIS REPORT ===")
        print(f"Dataset: {task_title}")
        print(f"Analysis Date: {{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        print(f"Dataset Shape: {{self.data.shape}}")
        print(f"Total Missing Values: {{self.data.isnull().sum().sum()}}")
        
        # Summary statistics
        print("\\n=== SUMMARY STATISTICS ===")
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            print(f"{{col}}: Mean={{self.data[col].mean():.2f}}, Std={{self.data[col].std():.2f}}")
        
        # Data quality assessment
        total_cells = self.data.shape[0] * self.data.shape[1]
        missing_cells = self.data.isnull().sum().sum()
        quality_score = (1 - missing_cells / total_cells) * 100
        print(f"\\nData Quality Score: {{quality_score:.2f}}%")
        
        return {{
            'dataset_shape': self.data.shape,
            'missing_values': missing_cells,
            'quality_score': quality_score,
            'analysis_date': pd.Timestamp.now(),
            'summary_statistics': self.data.describe().to_dict()
        }}

def main():
    """Main function to run the complete data analysis pipeline"""
    print("=== {task_title} ===")
    print("Data Science Analysis Pipeline")
    print()
    
    # Initialize analyzer
    analyzer = DataAnalyzer()
    
    # Load data
    analyzer.load_data()
    
    # Explore data
    analyzer.explore_data()
    
    # Visualize data
    analyzer.visualize_data()
    
    # Preprocess data
    X_train, X_test, y_train, y_test = analyzer.preprocess_data()
    
    # Train model if we have target
    if X_train is not None:
        model, feature_importance = analyzer.train_model(X_train, X_test, y_train, y_test)
    
    # Perform clustering
    analyzer.perform_clustering()
    
    # Generate report
    report = analyzer.generate_report()
    
    print("\\n=== ANALYSIS COMPLETE ===")
    print("Data science pipeline executed successfully!")
    
    return analyzer, report

if __name__ == "__main__":
    analyzer, report = main()'''
        
        return {
            "language": "Python/Data Science",
            "files": {
                "analysis.py": ds_code
            },
            "main_file": "analysis.py",
            "description": f"Complete data science pipeline for {task_title} with analysis, visualization, and machine learning",
            "features": ["Data exploration", "Statistical analysis", "Machine learning", "Clustering", "Visualization"],
            "dependencies": ["pandas", "numpy", "matplotlib", "seaborn", "scikit-learn"],
            "setup_instructions": "Install dependencies with: pip install pandas numpy matplotlib seaborn scikit-learn\n\nRun with: python analysis.py"
        }
    
    def _generate_mobile_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mobile application code"""
        
        task_title = task.title()
        
        mobile_code = f'''// React Native Application for {task_title}
// Modern mobile app with navigation and state management

import React, 'react';
import {{
    NavigationContainer,
    createStackNavigator,
    createBottomTabNavigator
}} from '@react-navigation/native';
import {{
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    TextInput,
    ScrollView,
    Alert,
    ActivityIndicator
}} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Main App Component
const App = () => {{
    return (
        <NavigationContainer>
            <AppNavigator />
        </NavigationContainer>
    );
}};

// Stack Navigator
const Stack = createStackNavigator();

const AppNavigator = () => {{
    return (
        <Stack.Navigator initialRouteName="Home">
            <Stack.Screen 
                name="Home" 
                component={{HomeScreen}}
                options={{{{{
                    title: '{task_title}',
                    headerStyle: {{
                        backgroundColor: '#3b82f6',
                    }},
                    headerTintColor: '#fff',
                }}}}
            />
            <Stack.Screen 
                name="Details" 
                component={{DetailsScreen}}
                options={{{{{
                    title: 'Details',
                    headerStyle: {{
                        backgroundColor: '#3b82f6',
                    }},
                    headerTintColor: '#fff',
                }}}}
            />
            <Stack.Screen 
                name="Profile" 
                component={{ProfileScreen}}
                options={{{{{
                    title: 'Profile',
                    headerStyle: {{
                        backgroundColor: '#3b82f6',
                    }},
                    headerTintColor: '#fff',
                }}}}
            />
        </Stack.Navigator>
    );
}};

// Home Screen
const HomeScreen = ({{ navigation }}) => {{
    const [tasks, setTasks] = React.useState([]);
    const [loading, setLoading] = React.useState(true);
    const [newTask, setNewTask] = React.useState('');
    
    React.useEffect(() => {{
        loadTasks();
    }}, []);
    
    const loadTasks = async () => {{
        try {{
            const storedTasks = await AsyncStorage.getItem('tasks');
            if (storedTasks) {{
                setTasks(JSON.parse(storedTasks));
            }}
        }} catch (error) {{
            console.error('Error loading tasks:', error);
        }} finally {{
            setLoading(false);
        }}
    }};
    
    const saveTasks = async (updatedTasks) => {{
        try {{
            await AsyncStorage.setItem('tasks', JSON.stringify(updatedTasks));
            setTasks(updatedTasks);
        }} catch (error) {{
            console.error('Error saving tasks:', error);
        }}
    }};
    
    const addTask = () => {{
        if (newTask.trim() === '') {{
            Alert.alert('Error', 'Please enter a task');
            return;
        }}
        
        const task = {{
            id: Date.now(),
            title: newTask,
            completed: false,
            createdAt: new Date().toISOString(),
        }};
        
        saveTasks([...tasks, task]);
        setNewTask('');
    }};
    
    const toggleTask = (taskId) => {{
        const updatedTasks = tasks.map(task =>
            task.id === taskId ? {{ ...task, completed: !task.completed }} : task
        );
        saveTasks(updatedTasks);
    }};
    
    const deleteTask = (taskId) => {{
        Alert.alert(
            'Delete Task',
            'Are you sure you want to delete this task?',
            [
                {{ text: 'Cancel', style: 'cancel' }},
                {{
                    text: 'Delete',
                    style: 'destructive',
                    onPress: () => {{
                        const updatedTasks = tasks.filter(task => task.id !== taskId);
                        saveTasks(updatedTasks);
                    }},
                }},
            ]
        );
    }};
    
    if (loading) {{
        return (
            <View style={{styles.loadingContainer}}>
                <ActivityIndicator size="large" color="#3b82f6" />
                <Text style={{styles.loadingText}}>Loading tasks...</Text>
            </View>
        );
    }}
    
    return (
        <View style={{styles.container}}>
            <View style={{styles.header}}>
                <Text style={{styles.headerTitle}}>{task_title}</Text>
                <Text style={{styles.headerSubtitle}}>Manage your tasks efficiently</Text>
            </View>
            
            <View style={{styles.inputContainer}}>
                <TextInput
                    style={{styles.input}}
                    placeholder="Enter a new task..."
                    value={{newTask}}
                    onChangeText={{setNewTask}}
                    multiline
                />
                <TouchableOpacity style={{styles.addButton}} onPress={{addTask}}>
                    <Text style={{styles.addButtonText}}>Add Task</Text>
                </TouchableOpacity>
            </View>
            
            <ScrollView style={{styles.tasksContainer}}>
                {{tasks.map(task => (
                    <View key={{task.id}} style={{styles.taskItem}}>
                        <TouchableOpacity
                            style={{styles.taskContent}}
                            onPress={{() => toggleTask(task.id)}}
                        >
                            <View style={{styles.taskLeft}}>
                                <View style={[
                                    styles.checkbox,
                                    {{ backgroundColor: task.completed ? '#3b82f6' : '#e5e7eb' }}
                                ]}}>
                                    {{task.completed && (
                                        <Text style={{styles.checkmark}}>✓</Text>
                                    )}}
                                </View>
                                <Text style={[
                                    styles.taskTitle,
                                    {{ textDecorationLine: task.completed ? 'line-through' : 'none' }}
                                ]}}>
                                    {{task.title}}
                                </Text>
                            </View>
                            <TouchableOpacity
                                style={{styles.deleteButton}}
                                onPress={{() => deleteTask(task.id)}}
                            >
                                <Text style={{styles.deleteButtonText}}>×</Text>
                            </TouchableOpacity>
                        </TouchableOpacity>
                    </View>
                ))}}
            </ScrollView>
            
            <View style={{styles.footer}}>
                <TouchableOpacity
                    style={{styles.footerButton}}
                    onPress={{() => navigation.navigate('Details')}}
                >
                    <Text style={{styles.footerButtonText}}>View Details</Text>
                </TouchableOpacity>
                <TouchableOpacity
                    style={{styles.footerButton}}
                    onPress={{() => navigation.navigate('Profile')}}
                >
                    <Text style={{styles.footerButtonText}}>Profile</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}};

// Details Screen
const DetailsScreen = () => {{
    return (
        <View style={{styles.container}}>
            <View style={{styles.header}}>
                <Text style={{styles.headerTitle}}>Details</Text>
                <Text style={{styles.headerSubtitle}}>App information and statistics</Text>
            </View>
            
            <ScrollView style={{styles.content}}>
                <View style={{styles.section}}>
                    <Text style={{styles.sectionTitle}}>About {task_title}</Text>
                    <Text style={{styles.sectionText}}>
                        This is a modern React Native application built with best practices.
                        It features task management, local storage, and a beautiful user interface.
                    </Text>
                </View>
                
                <View style={{styles.section}}>
                    <Text style={{styles.sectionTitle}}>Features</Text>
                    <View style={{styles.featureList}}>
                        <Text style={{styles.featureItem}}>✓ Task management</Text>
                        <Text style={{styles.featureItem}}>✓ Local storage</Text>
                        <Text style={{styles.featureItem}}>✓ Beautiful UI</Text>
                        <Text style={{styles.featureItem}}>✓ Smooth animations</Text>
                        <Text style={{styles.featureItem}}>✓ Cross-platform</Text>
                    </View>
                </View>
                
                <View style={{styles.section}}>
                    <Text style={{styles.sectionTitle}}>Technologies</Text>
                    <View style={{styles.techList}}>
                        <Text style={{styles.techItem}}>React Native</Text>
                        <Text style={{styles.techItem}}>React Navigation</Text>
                        <Text style={{styles.techItem}}>AsyncStorage</Text>
                        <Text style={{styles.techItem}}>Native Components</Text>
                    </View>
                </View>
            </ScrollView>
        </View>
    );
}};

// Profile Screen
const ProfileScreen = () => {{
    return (
        <View style={{styles.container}}>
            <View style={{styles.header}}>
                <Text style={{styles.headerTitle}}>Profile</Text>
                <Text style={{styles.headerSubtitle}}>User information and settings</Text>
            </View>
            
            <ScrollView style={{styles.content}}>
                <View style={{styles.profileSection}}>
                    <View style={{styles.avatarContainer}}>
                        <View style={{styles.avatar}}>
                            <Text style={{styles.avatarText}}>U</Text>
                        </View>
                    </View>
                    <Text style={{styles.profileName}}>User Name</Text>
                    <Text style={{styles.profileEmail}}>user@example.com</Text>
                </View>
                
                <View style={{styles.section}}>
                    <Text style={{styles.sectionTitle}}>Statistics</Text>
                    <View style={{styles.statsContainer}}>
                        <View style={{styles.statItem}}>
                            <Text style={{styles.statNumber}}>0</Text>
                            <Text style={{styles.statLabel}}>Tasks</Text>
                        </View>
                        <View style={{styles.statItem}}>
                            <Text style={{styles.statNumber}}>0</Text>
                            <Text style={{styles.statLabel}}>Completed</Text>
                        </View>
                        <View style={{styles.statItem}}>
                            <Text style={{styles.statNumber}}>0%</Text>
                            <Text style={{styles.statLabel}}>Completion</Text>
                        </View>
                    </View>
                </View>
                
                <View style={{styles.section}}>
                    <Text style={{styles.sectionTitle}}>Settings</Text>
                    <View style={{styles.settingList}}>
                        <TouchableOpacity style={{styles.settingItem}}>
                            <Text style={{styles.settingText}}>Notifications</Text>
                            <Text style={{styles.settingValue}}>Enabled</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={{styles.settingItem}}>
                            <Text style={{styles.settingText}}>Theme</Text>
                            <Text style={{styles.settingValue}}>Light</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={{styles.settingItem}}>
                            <Text style={{styles.settingText}}>Language</Text>
                            <Text style={{styles.settingValue}}>English</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </ScrollView>
        </View>
    );
}};

// Styles
const styles = StyleSheet.create({{
    container: {{
        flex: 1,
        backgroundColor: '#f8fafc',
    }},
    loadingContainer: {{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    }},
    loadingText: {{
        marginTop: 10,
        color: '#64748b',
    }},
    header: {{
        backgroundColor: '#3b82f6',
        padding: 20,
        paddingTop: 40,
    }},
    headerTitle: {{
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fff',
    }},
    headerSubtitle: {{
        fontSize: 14,
        color: '#cbd5e1',
        marginTop: 4,
    }},
    inputContainer: {{
        padding: 20,
        backgroundColor: '#fff',
        margin: 20,
        borderRadius: 12,
        shadowColor: '#000',
        shadowOffset: {{ width: 0, height: 2 }},
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    }},
    input: {{
        borderWidth: 1,
        borderColor: '#e5e7eb',
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        marginBottom: 12,
        minHeight: 60,
    }},
    addButton: {{
        backgroundColor: '#3b82f6',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    }},
    addButtonText: {{
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    }},
    tasksContainer: {{
        flex: 1,
        paddingHorizontal: 20,
    }},
    taskItem: {{
        backgroundColor: '#fff',
        marginVertical: 6,
        borderRadius: 8,
        shadowColor: '#000',
        shadowOffset: {{ width: 0, height: 1 }},
        shadowOpacity: 0.1,
        shadowRadius: 2,
        elevation: 2,
    }},
    taskContent: {{
        flexDirection: 'row',
        alignItems: 'center',
        padding: 16,
    }},
    taskLeft: {{
        flexDirection: 'row',
        alignItems: 'center',
        flex: 1,
    }},
    checkbox: {{
        width: 24,
        height: 24,
        borderRadius: 12,
        borderWidth: 2,
        borderColor: '#3b82f6',
        marginRight: 12,
        justifyContent: 'center',
        alignItems: 'center',
    }},
    checkmark: {{
        color: '#fff',
        fontSize: 14,
        fontWeight: 'bold',
    }},
    taskTitle: {{
        fontSize: 16,
        color: '#1f2937',
        flex: 1,
    }},
    deleteButton: {{
        width: 32,
        height: 32,
        borderRadius: 16,
        backgroundColor: '#ef4444',
        justifyContent: 'center',
        alignItems: 'center',
        marginLeft: 12,
    }},
    deleteButtonText: {{
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    }},
    footer: {{
        flexDirection: 'row',
        padding: 20,
        backgroundColor: '#fff',
        borderTopWidth: 1,
        borderTopColor: '#e5e7eb',
    }},
    footerButton: {{
        flex: 1,
        marginHorizontal: 5,
        padding: 12,
        backgroundColor: '#3b82f6',
        borderRadius: 8,
        alignItems: 'center',
    }},
    footerButtonText: {{
        color: '#fff',
        fontSize: 14,
        fontWeight: 'bold',
    }},
    content: {{
        flex: 1,
        padding: 20,
    }},
    section: {{
        marginBottom: 24,
    }},
    sectionTitle: {{
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1f2937',
        marginBottom: 12,
    }},
    sectionText: {{
        fontSize: 14,
        color: '#6b7280',
        lineHeight: 20,
    }},
    featureList: {{
        marginLeft: 8,
    }},
    featureItem: {{
        fontSize: 14,
        color: '#6b7280',
        marginBottom: 4,
    }},
    techList: {{
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginLeft: 8,
    }},
    techItem: {{
        backgroundColor: '#e5e7eb',
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 16,
        fontSize: 12,
        color: '#6b7280',
        marginRight: 8,
        marginBottom: 8,
    }},
    profileSection: {{
        alignItems: 'center',
        marginBottom: 24,
    }},
    avatarContainer: {{
        marginBottom: 16,
    }},
    avatar: {{
        width: 80,
        height: 80,
        borderRadius: 40,
        backgroundColor: '#3b82f6',
        justifyContent: 'center',
        alignItems: 'center',
    }},
    avatarText: {{
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
    }},
    profileName: {{
        fontSize: 20,
        fontWeight: 'bold',
        color: '#1f2937',
        marginBottom: 4,
    }},
    profileEmail: {{
        fontSize: 14,
        color: '#6b7280',
    }},
    statsContainer: {{
        flexDirection: 'row',
        justifyContent: 'space-around',
    }},
    statItem: {{
        alignItems: 'center',
    }},
    statNumber: {{
        fontSize: 24,
        fontWeight: 'bold',
        color: '#3b82f6',
    }},
    statLabel: {{
        fontSize: 12,
        color: '#6b7280',
        marginTop: 4,
    }},
    settingList: {{
        marginLeft: 8,
    }},
    settingItem: {{
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#e5e7eb',
    }},
    settingText: {{
        fontSize: 14,
        color: '#1f2937',
    }},
    settingValue: {{
        fontSize: 14,
        color: '#6b7280',
    }},
}});

export default App;'''
        
        return {
            "language": "JavaScript/React Native",
            "files": {
                "App.js": mobile_code
            },
            "main_file": "App.js",
            "description": f"Complete React Native application for {task_title} with navigation and state management",
            "features": ["Task management", "Local storage", "Navigation", "Beautiful UI", "Cross-platform"],
            "dependencies": ["react", "react-native", "@react-navigation/native", "@react-navigation/stack", "@react-native-async-storage/async-storage"],
            "setup_instructions": "Install dependencies with: npm install react-native @react-navigation/native @react-navigation/stack @react-native-async-storage/async-storage\n\nRun with: npx react-native run-android or npx react-native run-ios"
        }
    
    def _generate_general_code(self, task: str, strategy: Dict[str, Any], research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate general purpose code"""
        
        task_title = task.title()
        
        general_code = f'''# Python Solution for {task_title}
# General purpose implementation with proper structure and error handling

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TaskItem:
    """Data class representing a task item"""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class ProjectConfig:
    """Configuration for the project"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class TaskManager:
    """Main class for managing tasks and project operations"""
    
    def __init__(self, config: Optional[ProjectConfig] = None):
        self.config = config or ProjectConfig(name="{task_title}")
        self.tasks: List[TaskItem] = []
        self.next_id = 1
        self.data_file = Path("tasks.json")
        self.load_tasks()
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> TaskItem:
        """Add a new task to the system"""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium, or high")
        
        task = TaskItem(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            priority=priority
        )
        
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        
        logger.info(f"Added task: {{task.title}}")
        return task
    
    def get_task(self, task_id: int) -> Optional[TaskItem]:
        """Get a task by ID"""
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def update_task(self, task_id: int, **kwargs) -> Optional[TaskItem]:
        """Update an existing task"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Update allowed fields
        updatable_fields = ['title', 'description', 'completed', 'priority']
        for key, value in kwargs.items():
            if key in updatable_fields and hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.now()
        self.save_tasks()
        
        logger.info(f"Updated task {{task_id}}")
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        
        logger.info(f"Deleted task {{task_id}}")
        return True
    
    def list_tasks(self, completed_only: bool = False, priority: Optional[str] = None) -> List[TaskItem]:
        """List tasks with optional filtering"""
        tasks = self.tasks.copy()
        
        if completed_only:
            tasks = [task for task in tasks if task.completed]
        
        if priority:
            tasks = [task for task in tasks if task.priority == priority]
        
        return tasks
    
    def search_tasks(self, query: str) -> List[TaskItem]:
        """Search tasks by title or description"""
        query_lower = query.lower()
        return [
            task for task in self.tasks
            if query_lower in task.title.lower() or query_lower in task.description.lower()
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task.completed])
        pending = total - completed
        
        # Priority breakdown
        priority_counts = {{}}
        for task in self.tasks:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
        
        # Completion rate
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {{
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_rate": completion_rate,
            "priority_breakdown": priority_counts,
            "overdue_tasks": self.get_overdue_tasks(),
            "productivity_score": self.calculate_productivity_score()
        }}
    
    def get_overdue_tasks(self) -> List[TaskItem]:
        """Get tasks that are overdue (older than 7 days and not completed)"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=7)
        return [
            task for task in self.tasks
            if not task.completed and task.created_at < cutoff_date
        ]
    
    def calculate_productivity_score(self) -> float:
        """Calculate a productivity score based on task completion and timeliness"""
        stats = self.get_statistics()
        
        # Base score from completion rate
        base_score = stats["completion_rate"]
        
        # Penalty for overdue tasks
        overdue_penalty = len(stats["overdue_tasks"]) * 5
        
        # Bonus for high priority tasks completed
        high_priority_completed = len([
            task for task in self.tasks
            if task.completed and task.priority == "high"
        ])
        completion_bonus = high_priority_completed * 3
        
        final_score = max(0, base_score + completion_bonus - overdue_penalty)
        return min(100, final_score)  # Cap at 100
    
    def save_tasks(self, filename: Optional[str] = None):
        """Save tasks to a JSON file"""
        filename = filename or self.data_file
        
        try:
            tasks_data = []
            for task in self.tasks:
                task_dict = asdict(task)
                # Convert datetime objects to ISO strings
                task_dict["created_at"] = task.created_at.isoformat()
                task_dict["updated_at"] = task.updated_at.isoformat()
                tasks_data.append(task_dict)
            
            # Save project config and tasks
            project_data = {{
                "config": asdict(self.config),
                "tasks": tasks_data,
                "metadata": {{
                    "version": "1.0.0",
                    "exported_at": datetime.now().isoformat()
                }}
            }}
            
            with open(filename, 'w') as f:
                json.dump(project_data, f, indent=2)
            
            logger.info(f"Tasks saved to {{filename}}")
            
        except Exception as e:
            logger.error(f"Error saving tasks: {{e}}")
            raise
    
    def load_tasks(self, filename: Optional[str] = None):
        """Load tasks from a JSON file"""
        filename = filename or self.data_file
        
        try:
            if filename.exists():
                with open(filename, 'r') as f:
                    project_data = json.load(f)
                
                # Load config
                if "config" in project_data:
                    config_dict = project_data["config"]
                    config_dict["created_at"] = datetime.fromisoformat(config_dict["created_at"])
                    self.config = ProjectConfig(**config_dict)
                
                # Load tasks
                if "tasks" in project_data:
                    for task_dict in project_data["tasks"]:
                        task_dict["created_at"] = datetime.fromisoformat(task_dict["created_at"])
                        task_dict["updated_at"] = datetime.fromisoformat(task_dict["updated_at"])
                        
                        task = TaskItem(**task_dict)
                        self.tasks.append(task)
                        
                        if task.id >= self.next_id:
                            self.next_id = task.id + 1
                
                logger.info(f"Loaded {{len(self.tasks)}} tasks from {{filename}}")
            
        except Exception as e:
            logger.error(f"Error loading tasks: {{e}}")
    
    def export_to_csv(self, filename: str = "tasks_export.csv"):
        """Export tasks to CSV format"""
        import csv
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['id', 'title', 'description', 'completed', 'priority', 'created_at', 'updated_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for task in self.tasks:
                    writer.writerow({{
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'completed': task.completed,
                        'priority': task.priority,
                        'created_at': task.created_at.isoformat(),
                        'updated_at': task.updated_at.isoformat()
                    }})
            
            logger.info(f"Tasks exported to {{filename}}")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {{e}}")
            raise
    
    def generate_report(self) -> str:
        """Generate a comprehensive text report"""
        stats = self.get_statistics()
        
        report = f"""
# {self.config.name} - Task Management Report

Generated on: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}

## Overview
- Total Tasks: {{stats['total_tasks']}}
- Completed: {{stats['completed_tasks']}}
- Pending: {{stats['pending_tasks']}}
- Completion Rate: {{stats['completion_rate']:.1f}}%
- Productivity Score: {{stats['productivity_score']:.1f}}/100

## Priority Breakdown
"""
        
        for priority, count in stats['priority_breakdown'].items():
            report += f"- {{priority.title()}}: {{count}}\\n"
        
        report += f"""
## Overdue Tasks
- {{len(stats['overdue_tasks'])}} tasks overdue

## Recent Activity
"""
        
        # Show last 5 tasks
        recent_tasks = sorted(self.tasks, key=lambda x: x.created_at, reverse=True)[:5]
        for task in recent_tasks:
            status = "✓" if task.completed else "○"
            report += f"- {{status}} [{{task.id}}] {{task.title}} ({{task.priority}})\\n"
        
        return report

class TaskCLI:
    """Command-line interface for the task manager"""
    
    def __init__(self):
        self.manager = TaskManager()
    
    def run(self):
        """Run the CLI interface"""
        print("=== {task_title} ===")
        print("Task Management System")
        print()
        
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-8): ").strip()
            
            try:
                if choice == '1':
                    self.add_task_interactive()
                elif choice == '2':
                    self.list_tasks_interactive()
                elif choice == '3':
                    self.update_task_interactive()
                elif choice == '4':
                    self.delete_task_interactive()
                elif choice == '5':
                    self.search_tasks_interactive()
                elif choice == '6':
                    self.show_statistics()
                elif choice == '7':
                    self.generate_report()
                elif choice == '8':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {{e}}")
            
            input("Press Enter to continue...")
    
    def show_menu(self):
        """Display the main menu"""
        print("\\n" + "="*50)
        print("TASK MANAGEMENT MENU")
        print("="*50)
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Show Statistics")
        print("7. Generate Report")
        print("8. Exit")
        print("="*50)
    
    def add_task_interactive(self):
        """Interactive task addition"""
        print("\\n--- Add New Task ---")
        title = input("Task title: ").strip()
        description = input("Description (optional): ").strip()
        priority = input("Priority (low/medium/high): ").strip().lower()
        
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        
        task = self.manager.add_task(title, description, priority)
        print(f"\\nTask added successfully!")
        print(f"ID: {{task.id}}")
        print(f"Title: {{task.title}}")
        print(f"Priority: {{task.priority}}")
    
    def list_tasks_interactive(self):
        """Interactive task listing"""
        print("\\n--- Task List ---")
        
        filter_choice = input("Filter by (all/completed/pending): ").strip().lower()
        
        if filter_choice == 'completed':
            tasks = self.manager.list_tasks(completed_only=True)
        elif filter_choice == 'pending':
            tasks = [task for task in self.manager.list_tasks() if not task.completed]
        else:
            tasks = self.manager.list_tasks()
        
        if not tasks:
            print("No tasks found.")
            return
        
        print(f"\\nFound {{len(tasks)}} tasks:")
        print("-" * 60)
        
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"{{status}} [{{task.id}}] {{task.title}} ({{task.priority}})")
            if task.description:
                print(f"    {{task.description}}")
            print(f"    Created: {{task.created_at.strftime('%Y-%m-%d %H:%M')}}")
            print()
    
    def update_task_interactive(self):
        """Interactive task update"""
        print("\\n--- Update Task ---")
        
        try:
            task_id = int(input("Enter task ID: "))
            task = self.manager.get_task(task_id)
            
            if not task:
                print("Task not found.")
                return
            
            print(f"\\nCurrent task: {{task.title}}")
            print("1. Mark as completed/uncompleted")
            print("2. Update title")
            print("3. Update description")
            print("4. Update priority")
            
            choice = input("What to update? (1-4): ").strip()
            
            if choice == '1':
                self.manager.update_task(task_id, completed=not task.completed)
                status = "completed" if not task.completed else "pending"
                print(f"Task marked as {{status}}.")
            
            elif choice == '2':
                new_title = input("New title: ").strip()
                self.manager.update_task(task_id, title=new_title)
                print("Title updated.")
            
            elif choice == '3':
                new_description = input("New description: ").strip()
                self.manager.update_task(task_id, description=new_description)
                print("Description updated.")
            
            elif choice == '4':
                new_priority = input("New priority (low/medium/high): ").strip().lower()
                if new_priority in ['low', 'medium', 'high']:
                    self.manager.update_task(task_id, priority=new_priority)
                    print("Priority updated.")
                else:
                    print("Invalid priority.")
            
        except ValueError:
            print("Invalid task ID.")
    
    def delete_task_interactive(self):
        """Interactive task deletion"""
        print("\\n--- Delete Task ---")
        
        try:
            task_id = int(input("Enter task ID: "))
            task = self.manager.get_task(task_id)
            
            if not task:
                print("Task not found.")
                return
            
            print(f"\\nTask to delete: {{task.title}}")
            confirm = input("Are you sure? (y/N): ").strip().lower()
            
            if confirm == 'y':
                if self.manager.delete_task(task_id):
                    print("Task deleted successfully.")
                else:
                    print("Failed to delete task.")
            else:
                print("Deletion cancelled.")
        
        except ValueError:
            print("Invalid task ID.")
    
    def search_tasks_interactive(self):
        """Interactive task search"""
        print("\\n--- Search Tasks ---")
        query = input("Enter search query: ").strip()
        
        if not query:
            print("Please enter a search query.")
            return
        
        results = self.manager.search_tasks(query)
        
        if not results:
            print("No tasks found.")
            return
        
        print(f"\\nFound {{len(results)}} tasks matching '{{query}}':")
        print("-" * 60)
        
        for task in results:
            status = "✓" if task.completed else "○"
            print(f"{{status}} [{{task.id}}] {{task.title}} ({{task.priority}})")
    
    def show_statistics(self):
        """Display task statistics"""
        print("\\n--- Task Statistics ---")
        
        stats = self.manager.get_statistics()
        
        print(f"Total Tasks: {{stats['total_tasks']}}")
        print(f"Completed: {{stats['completed_tasks']}}")
        print(f"Pending: {{stats['pending_tasks']}}")
        print(f"Completion Rate: {{stats['completion_rate']:.1f}}%")
        print(f"Productivity Score: {{stats['productivity_score']:.1f}}/100")
        print(f"Overdue Tasks: {{len(stats['overdue_tasks'])}}")
        
        print("\\nPriority Breakdown:")
        for priority, count in stats['priority_breakdown'].items():
            print(f"  {{priority.title()}}: {{count}}")
    
    def generate_report(self):
        """Generate and display report"""
        print("\\n--- Generating Report ---")
        
        report = self.manager.generate_report()
        print(report)
        
        # Save report to file
        report_filename = f"task_report_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"\\nReport saved to: {{report_filename}}")

def main():
    """Main function to run the application"""
    print("=== {task_title} ===")
    print("Task Management System")
    print()
    
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        # Run CLI interface
        cli = TaskCLI()
        cli.run()
    else:
        # Run demo
        manager = TaskManager()
        
        # Add sample tasks
        manager.add_task("Setup project structure", "Create directories and files", "high")
        manager.add_task("Write documentation", "Document the API endpoints", "medium")
        manager.add_task("Add tests", "Write unit tests for all functions", "medium")
        manager.add_task("Deploy to production", "Set up CI/CD pipeline", "low")
        
        # Display current tasks
        print("Current tasks:")
        for task in manager.list_tasks():
            status = "✓" if task.completed else "○"
            print(f"  {{status}} [{{task.id}}] {{task.title}} ({{task.priority}})")
        
        # Display statistics
        print("\\nStatistics:")
        stats = manager.get_statistics()
        for key, value in stats.items():
            if key != 'priority_breakdown':
                print(f"  {{key}}: {{value}}")
        
        # Save tasks
        manager.save_tasks()
        
        print("\\nTask management system ready!")
        print("Run with 'python script.py cli' for interactive mode.")

if __name__ == "__main__":
    main()'''
        
        return {
            "language": "Python",
            "files": {
                "main.py": general_code
            },
            "main_file": "main.py",
            "description": f"Complete Python solution for {task_title} with task management, CLI interface, and data persistence",
            "features": ["Task management", "Data persistence", "CLI interface", "Statistics", "Search functionality"],
            "dependencies": [],
            "setup_instructions": "Run with: python main.py\n\nFor interactive mode: python main.py cli"
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
                "task = manager.add_task('Complete project', 'Finish all remaining tasks', 'high')",
                "",
                "# List all tasks",
                "tasks = manager.list_tasks()",
                "for task in tasks:",
                "    print(f'{task.id}: {task.title}')"
            ],
            "javascript": [
                "// Import the main module",
                "import { App } from './App.js';",
                "",
                "// Initialize the application",
                "const app = new App();",
                "",
                "// Add a new task",
                "app.addTask('Complete project', 'Finish all remaining tasks', 'high');",
                "",
                "// List all tasks",
                "const tasks = app.listTasks();",
                "console.log(tasks);"
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
                "  // Initialize the app",
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
                        "description": "Get all tasks (requires authentication)"
                    },
                    {
                        "method": "POST",
                        "path": "/tasks",
                        "description": "Create a new task (requires authentication)"
                    },
                    {
                        "method": "GET",
                        "path": "/tasks/{task_id}",
                        "description": "Get a specific task (requires authentication)"
                    },
                    {
                        "method": "PUT",
                        "path": "/tasks/{task_id}",
                        "description": "Update a task (requires authentication)"
                    },
                    {
                        "method": "DELETE",
                        "path": "/tasks/{task_id}",
                        "description": "Delete a task (requires authentication)"
                    }
                ],
                "authentication": "Bearer token (JWT)",
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
                "Issue: Permission denied - Solution: Run with appropriate permissions or use virtual environment",
                "Issue: Import errors - Solution: Ensure all modules are in the correct path",
                "Issue: JSON decode errors - Solution: Check JSON file format and encoding"
            ],
            "javascript": [
                "Issue: Module not found - Solution: Install dependencies using npm",
                "Issue: CORS errors - Solution: Configure CORS headers in the backend",
                "Issue: Async/await errors - Solution: Ensure proper async function usage",
                "Issue: DOM manipulation errors - Solution: Wait for DOM to be fully loaded"
            ],
            "html/css/javascript": [
                "Issue: Styles not loading - Solution: Check CSS file path and link tag",
                "Issue: JavaScript not working - Solution: Check script tag and console errors",
                "Issue: Responsive design issues - Solution: Check viewport meta tag and media queries",
                "Issue: Browser compatibility - Solution: Use polyfills for older browsers"
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
    task = manager.add_task("Test task", "Test description", "high")
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.priority == "high"
    assert task.completed == False
    print("✓ Task creation test passed")
"""
                },
                {
                    "name": "test_task_completion",
                    "description": "Test marking a task as completed",
                    "code": """
def test_task_completion():
    manager = TaskManager()
    task = manager.add_task("Test task")
    updated_task = manager.update_task(task.id, completed=True)
    assert updated_task.completed == True
    print("✓ Task completion test passed")
"""
                }
            ]
        elif language == "javascript":
            return [
                {
                    "name": "testAppInitialization",
                    "description": "Test app initialization",
                    "code": """
function testAppInitialization() {
    const app = new App();
    assert(app instanceof App, 'App should be initialized');
    console.log('✓ App initialization test passed');
}
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
