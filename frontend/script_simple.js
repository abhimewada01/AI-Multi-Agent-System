// AI Multi-Agent System - Simplified Frontend JavaScript

class AIMultiAgentSystem {
    constructor() {
        this.apiBase = "http://127.0.0.1:8000";
        this.currentTask = null;
        this.results = null;
        this.isProcessing = false;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkServerStatus();
        this.initializeTabs();
    }

    bindEvents() {
        // Submit button
        document.getElementById('submitBtn').addEventListener('click', () => this.handleSubmit());
        
        // Clear button
        document.getElementById('clearBtn').addEventListener('click', () => this.clearInput());
        
        // Task input - enable/disable submit button
        document.getElementById('taskInput').addEventListener('input', (e) => {
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = !e.target.value.trim() || this.isProcessing;
        });
        
        // Tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Modal close
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        
        // Modal backdrop click
        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') this.closeModal();
        });
        
        // About button
        document.getElementById('aboutBtn').addEventListener('click', (e) => {
            e.preventDefault();
            this.showAbout();
        });
        
        // Help button
        document.getElementById('helpBtn').addEventListener('click', (e) => {
            e.preventDefault();
            this.showHelp();
        });
        
        // Enter key in task input
        document.getElementById('taskInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });
    }

    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateServerStatus('connected', 'Connected');
            } else {
                this.updateServerStatus('error', 'Server Error');
            }
        } catch (error) {
            console.error('Server status check failed:', error);
            this.updateServerStatus('error', 'Disconnected');
        }
    }

    updateServerStatus(status, text) {
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        statusDot.className = `status-dot ${status}`;
        statusText.textContent = text;
    }

    async handleSubmit() {
        const taskInput = document.getElementById('taskInput');
        const task = taskInput.value.trim();
        
        if (!task || this.isProcessing) return;
        
        this.currentTask = task;
        this.isProcessing = true;
        this.updateUIState('processing');
        this.showLoading(true);
        
        // Reset agent states
        this.resetAgentStates();
        
        try {
            // Use the correct endpoint as specified
            const response = await fetch(`${this.apiBase}/process-task`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ task: task })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const results = await response.json();
            this.results = results;
            
            // Update UI with results
            await this.displayResults(results);
            
            // Show completion
            this.showCompletion();
            
        } catch (error) {
            console.error('Processing failed:', error);
            this.showError('Processing failed: ' + error.message);
        } finally {
            this.isProcessing = false;
            this.updateUIState('ready');
            this.showLoading(false);
        }
    }

    resetAgentStates() {
        const agents = ['research', 'planning', 'coding', 'execution'];
        
        agents.forEach(agent => {
            const card = document.getElementById(`${agent}Agent`);
            const status = card.querySelector('.agent-status');
            const progress = document.getElementById(`${agent}Progress`);
            const result = document.getElementById(`${agent}Result`);
            
            card.classList.remove('active', 'completed');
            status.textContent = 'Waiting';
            status.className = 'agent-status';
            progress.style.width = '0%';
            result.innerHTML = '';
        });
    }

    async displayResults(results) {
        // Display results for each agent with progress animation
        await this.displayAgentProgress('research', results.research);
        await this.displayAgentProgress('planning', results.plan);
        await this.displayAgentProgress('coding', results.code);
        await this.displayAgentProgress('execution', results.execution);
        
        // Display summary
        this.displaySummary(results);
        
        // Display detailed results in tabs
        this.displayDetailedResults(results);
    }

    async displayAgentProgress(agentType, result) {
        if (!result) return;
        
        const card = document.getElementById(`${agentType}Agent`);
        const status = card.querySelector('.agent-status');
        const progress = document.getElementById(`${agentType}Progress`);
        const resultDiv = document.getElementById(`${agentType}Result`);
        
        // Update status to processing
        status.textContent = 'Processing';
        status.className = 'agent-status processing';
        card.classList.add('active');
        
        // Animate progress
        await this.animateProgress(progress, 100);
        
        // Update to completed
        status.textContent = 'Completed';
        status.className = 'agent-status completed';
        
        // Display result
        resultDiv.innerHTML = `<p><strong>Status:</strong> ${status.textContent}</p><p>${result}</p>`;
        
        // Add completion class
        setTimeout(() => {
            card.classList.add('completed');
        }, 500);
    }

    async animateProgress(progressElement, targetWidth) {
        return new Promise(resolve => {
            let width = 0;
            const increment = targetWidth / 20;
            const interval = setInterval(() => {
                width += increment;
                if (width >= targetWidth) {
                    width = targetWidth;
                    clearInterval(interval);
                    resolve();
                }
                progressElement.style.width = `${width}%`;
            }, 50);
        });
    }

    displaySummary(results) {
        const summaryContent = document.getElementById('summaryContent');
        
        const summaryHTML = `
            <div class="summary-card">
                <h3>Task Summary</h3>
                <p><strong>Original Task:</strong> ${this.currentTask}</p>
                <p><strong>Processing Time:</strong> ${results.total_time ? `${results.total_time.toFixed(2)}s` : 'N/A'}</p>
                
                <h4>Agent Results</h4>
                <ul>
                    <li><strong>Research Agent:</strong> ${results.research || 'Completed'}</li>
                    <li><strong>Planning Agent:</strong> ${results.plan || 'Completed'}</li>
                    <li><strong>Coding Agent:</strong> ${results.code || 'Completed'}</li>
                    <li><strong>Execution Agent:</strong> ${results.execution || 'Completed'}</li>
                </ul>
                
                <h4>Final Output</h4>
                <div class="final-output">
                    ${this.formatText(results.execution || 'No final output available')}
                </div>
            </div>
        `;
        
        summaryContent.innerHTML = summaryHTML;
    }

    displayDetailedResults(results) {
        // Update all tabs with results
        document.getElementById('researchContent').innerHTML = `
            <h3>Research Results</h3>
            <div class="detail-section">
                <p>${this.formatText(results.research || 'No research results available')}</p>
            </div>
        `;
        
        document.getElementById('planningContent').innerHTML = `
            <h3>Planning Results</h3>
            <div class="detail-section">
                <p>${this.formatText(results.plan || 'No planning results available')}</p>
            </div>
        `;
        
        document.getElementById('codeContent').innerHTML = `
            <h3>Code Results</h3>
            <div class="detail-section">
                <p>${this.formatText(results.code || 'No code results available')}</p>
            </div>
        `;
        
        document.getElementById('finalContent').innerHTML = `
            <h3>Final Output</h3>
            <div class="detail-section">
                <p>${this.formatText(results.execution || 'No final output available')}</p>
            </div>
        `;
    }

    formatText(text) {
        if (!text) return '';
        return text.split('\n').map(line => line.trim() ? `<p>${line}</p>` : '').join('');
    }

    initializeTabs() {
        // Set first tab as active
        this.switchTab('summary');
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
        
        // Update tab panes
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        
        const activePane = document.getElementById(tabName);
        if (activePane) {
            activePane.classList.add('active');
        }
    }

    updateUIState(state) {
        const submitBtn = document.getElementById('submitBtn');
        const taskInput = document.getElementById('taskInput');
        
        if (state === 'processing') {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            taskInput.disabled = true;
        } else {
            submitBtn.disabled = !taskInput.value.trim();
            submitBtn.innerHTML = '<i class="fas fa-play"></i> Start Processing';
            taskInput.disabled = false;
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }

    showError(message) {
        this.showModal('Error', `<p style="color: var(--danger-color);">${message}</p>`);
    }

    showCompletion() {
        this.showModal('Task Completed!', `
            <p>Your task has been processed successfully by all AI agents.</p>
            <p>Check the Results section below to see the detailed output from each agent.</p>
        `);
    }

    showModal(title, content) {
        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        modalTitle.textContent = title;
        modalBody.innerHTML = content;
        modal.classList.add('active');
    }

    closeModal() {
        const modal = document.getElementById('modal');
        modal.classList.remove('active');
    }

    showAbout() {
        this.showModal('About AI Multi-Agent System', `
            <div class="about-content">
                <h4>System Overview</h4>
                <p>The AI Multi-Agent System is a platform where multiple intelligent AI agents collaborate to solve complex tasks through a structured workflow.</p>
                
                <h4>How It Works</h4>
                <ol>
                    <li><strong>Research Agent:</strong> Gathers and analyzes information about your task</li>
                    <li><strong>Planning Agent:</strong> Creates detailed step-by-step execution plans</li>
                    <li><strong>Coding Agent:</strong> Generates technical solutions and code</li>
                    <li><strong>Execution Agent:</strong> Synthesizes all results into comprehensive final outputs</li>
                </ol>
                
                <h4>Version</h4>
                <p>Version 1.0.0</p>
            </div>
        `);
    }

    showHelp() {
        this.showModal('Help & Usage Guide', `
            <div class="help-content">
                <h4>Getting Started</h4>
                <p>Simply enter your task in the input field and click "Start Processing". The system will coordinate all AI agents to complete your request.</p>
                
                <h4>Example Tasks</h4>
                <ul>
                    <li>"Build a simple Python REST API for user management"</li>
                    <li>"Explain machine learning with code examples"</li>
                    <li>"Create a web scraping script for data collection"</li>
                </ul>
                
                <h4>Tips</h4>
                <ul>
                    <li>Be specific in your task description for better results</li>
                    <li>Use Ctrl+Enter to quickly submit your task</li>
                    <li>Check the agent progress cards to see real-time status</li>
                </ul>
            </div>
        `);
    }

    clearInput() {
        document.getElementById('taskInput').value = '';
        document.getElementById('submitBtn').disabled = true;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AIMultiAgentSystem();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Check server status when page becomes visible again
        if (window.app) {
            window.app.checkServerStatus();
        }
    }
});

// Handle connection errors
window.addEventListener('online', () => {
    if (window.app) {
        window.app.checkServerStatus();
    }
});

window.addEventListener('offline', () => {
    if (window.app) {
        window.app.updateServerStatus('error', 'Offline');
    }
});
