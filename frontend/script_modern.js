// AI Multi-Agent System - Modern Professional Dashboard
// Advanced frontend with glassmorphism, workflow visualization, and enhanced features

class AIMultiAgentSystem {
    constructor() {
        this.apiBase = "http://127.0.0.1:8002";
        this.currentTask = null;
        this.results = null;
        this.isProcessing = false;
        this.agentTimers = {};
        this.taskHistory = this.loadTaskHistory();
        this.darkMode = false;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeLucideIcons();
        this.loadTaskHistory();
        this.setupKeyboardShortcuts();
        this.checkServerStatus();
    }

    initializeLucideIcons() {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    bindEvents() {
        // Main action buttons
        document.getElementById('runBtn').addEventListener('click', () => this.handleSubmit());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearInput());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadProject());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryTask());
        
        // Code actions
        document.getElementById('copyCodeBtn').addEventListener('click', () => this.copyCode());
        document.getElementById('downloadCodeBtn').addEventListener('click', () => this.downloadCode());
        
        // Dark mode toggle
        document.getElementById('darkModeToggle').addEventListener('click', () => this.toggleDarkMode());
        
        // Example prompts
        document.querySelectorAll('.example-prompt').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const prompt = e.currentTarget.dataset.prompt;
                document.getElementById('taskInput').value = prompt;
            });
        });
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Task input
        const taskInput = document.getElementById('taskInput');
        taskInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.handleSubmit();
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to run
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                if (!this.isProcessing) {
                    this.handleSubmit();
                }
            }
            
            // Escape to clear
            if (e.key === 'Escape') {
                this.clearInput();
            }
            
            // Ctrl/Cmd + D to toggle dark mode
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                this.toggleDarkMode();
            }
        });
    }

    toggleDarkMode() {
        this.darkMode = !this.darkMode;
        document.body.classList.toggle('dark-mode');
        
        const icon = document.querySelector('#darkModeToggle i');
        icon.setAttribute('data-lucide', this.darkMode ? 'sun' : 'moon');
        lucide.createIcons();
        
        localStorage.setItem('darkMode', this.darkMode);
    }

    loadTaskHistory() {
        const saved = localStorage.getItem('taskHistory');
        return saved ? JSON.parse(saved) : [];
    }

    saveTaskToHistory(task) {
        this.taskHistory.unshift({
            task: task,
            timestamp: new Date().toISOString(),
            id: Date.now()
        });
        
        // Keep only last 10 tasks
        this.taskHistory = this.taskHistory.slice(0, 10);
        localStorage.setItem('taskHistory', JSON.stringify(this.taskHistory));
        this.displayTaskHistory();
    }

    displayTaskHistory() {
        const container = document.getElementById('recentTasks');
        container.innerHTML = '';
        
        this.taskHistory.forEach(item => {
            const taskEl = document.createElement('div');
            taskEl.className = 'sidebar-item p-3 rounded-lg text-white/80 cursor-pointer text-sm';
            taskEl.innerHTML = `
                <div class="truncate">${item.task}</div>
                <div class="text-xs text-white/40">${this.formatTime(item.timestamp)}</div>
            `;
            taskEl.addEventListener('click', () => {
                document.getElementById('taskInput').value = item.task;
            });
            container.appendChild(taskEl);
        });
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    }

    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            this.updateServerStatus(data.status === 'healthy');
        } catch (error) {
            this.updateServerStatus(false);
        }
    }

    updateServerStatus(isHealthy) {
        // Could add a status indicator in the header
        console.log('Server status:', isHealthy ? 'Healthy' : 'Unhealthy');
    }

    async handleSubmit() {
        const taskInput = document.getElementById('taskInput');
        const task = taskInput.value.trim();
        
        if (!task) {
            this.showError('Please enter a task');
            return;
        }
        
        if (this.isProcessing) {
            return;
        }
        
        this.currentTask = task;
        this.isProcessing = true;
        this.saveTaskToHistory(task);
        
        // Hide previous results and errors
        this.hideResults();
        this.hideError();
        
        // Update UI state
        this.updateRunButton(true);
        this.resetAgentStates();
        this.resetWorkflow();
        
        try {
            this.logDebug('Starting task processing', { task });
            
            const response = await fetch(`${this.apiBase}/process-task`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const results = await response.json();
            this.logDebug('Task completed successfully', results);
            
            await this.displayResults(results);
            
        } catch (error) {
            this.logDebug('Task failed', error);
            this.showError(`Processing failed: ${error.message}`);
        } finally {
            this.isProcessing = false;
            this.updateRunButton(false);
        }
    }

    async displayResults(results) {
        this.results = results;
        
        // Display results for each agent with timing
        await this.displayAgentResult('research', results.research, 0.5);
        await this.displayAgentResult('planning', results.plan, 0.5);
        await this.displayCodeResult(results.code, 0.5);
        await this.displayAgentResult('execution', results.execution, 0.5);
        
        // Update workflow visualization
        this.updateWorkflow();
        
        // Display summary with quality assessment
        this.displaySummary(results);
        
        // Show results section
        this.showResults();
        
        // Update tab contents
        this.updateTabContents(results);
    }

    async displayAgentResult(agentType, result, delay = 0) {
        const startTime = Date.now();
        
        // Update workflow step
        const stepEl = document.getElementById(`${agentType}Step`);
        stepEl.classList.remove('bg-gray-600');
        stepEl.classList.add('bg-yellow-500', 'animate-pulse');
        
        // Update status
        const statusEl = document.getElementById(`${agentType}Status`);
        statusEl.textContent = 'Running';
        statusEl.className = 'px-2 py-1 rounded-full text-xs font-medium bg-yellow-500 text-white';
        
        // Animate progress
        const progressEl = document.getElementById(`${agentType}Progress`);
        const timeEl = document.getElementById(`${agentType}Time`);
        
        await this.animateProgress(progressEl, 100, delay);
        
        // Update to completed
        stepEl.classList.remove('bg-yellow-500', 'animate-pulse');
        stepEl.classList.add('bg-green-500');
        
        statusEl.textContent = 'Completed';
        statusEl.className = 'px-2 py-1 rounded-full text-xs font-medium bg-green-500 text-white';
        
        // Display result
        const resultEl = document.getElementById(`${agentType}Result`);
        resultEl.innerHTML = `<div class="text-sm leading-relaxed">${this.formatText(result)}</div>`;
        
        // Update timing
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        timeEl.textContent = `${elapsed}s`;
        
        // Add completion animation
        resultEl.classList.add('animate-fade-in');
    }

    async displayCodeResult(codeData, delay = 0) {
        const startTime = Date.now();
        
        // Update workflow step
        const stepEl = document.getElementById('codingStep');
        stepEl.classList.remove('bg-gray-600');
        stepEl.classList.add('bg-yellow-500', 'animate-pulse');
        
        // Update status
        const statusEl = document.getElementById('codingStatus');
        statusEl.textContent = 'Running';
        statusEl.className = 'px-2 py-1 rounded-full text-xs font-medium bg-yellow-500 text-white';
        
        // Animate progress
        const progressEl = document.getElementById('codingProgress');
        const timeEl = document.getElementById('codingTime');
        
        await this.animateProgress(progressEl, 100, delay);
        
        // Update to completed
        stepEl.classList.remove('bg-yellow-500', 'animate-pulse');
        stepEl.classList.add('bg-green-500');
        
        statusEl.textContent = 'Completed';
        statusEl.className = 'px-2 py-1 rounded-full text-xs font-medium bg-green-500 text-white';
        
        // Handle different code data formats
        let codeContent = '';
        let language = 'text';
        
        if (typeof codeData === 'object' && codeData.code) {
            language = codeData.language || 'text';
            codeContent = `
                <div class="mb-3">
                    <span class="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">${codeData.language || 'Unknown'}</span>
                </div>
                <div class="text-sm mb-2 text-white/60">${codeData.summary || 'Code generated successfully'}</div>
            `;
        }
        
        // Display result
        const resultEl = document.getElementById('codingResult');
        resultEl.innerHTML = codeContent + `<div class="text-sm">✨ Code generated successfully</div>`;
        
        // Update timing
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        timeEl.textContent = `${elapsed}s`;
        
        // Add completion animation
        resultEl.classList.add('animate-fade-in');
    }

    async animateProgress(element, targetWidth, duration = 1000) {
        return new Promise(resolve => {
            const startTime = Date.now();
            const startWidth = 0;
            
            const animate = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const width = startWidth + (targetWidth - startWidth) * progress;
                
                element.style.width = `${width}%`;
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    resolve();
                }
            };
            
            requestAnimationFrame(animate);
        });
    }

    updateWorkflow() {
        // Update all workflow steps to completed
        const steps = ['research', 'planning', 'coding', 'execution'];
        steps.forEach(step => {
            const stepEl = document.getElementById(`${step}Step`);
            stepEl.classList.remove('bg-gray-600', 'bg-yellow-500', 'animate-pulse');
            stepEl.classList.add('bg-green-500');
        });
    }

    resetWorkflow() {
        // Reset all workflow steps
        const steps = ['research', 'planning', 'coding', 'execution'];
        steps.forEach(step => {
            const stepEl = document.getElementById(`${step}Step`);
            stepEl.classList.remove('bg-green-500', 'bg-yellow-500', 'animate-pulse');
            stepEl.classList.add('bg-gray-600');
        });
    }

    resetAgentStates() {
        // Reset all agent cards
        const agents = ['research', 'planning', 'coding', 'execution'];
        agents.forEach(agent => {
            // Reset status
            const statusEl = document.getElementById(`${agent}Status`);
            statusEl.textContent = 'Waiting';
            statusEl.className = 'px-2 py-1 rounded-full text-xs font-medium bg-gray-600 text-white';
            
            // Reset progress
            const progressEl = document.getElementById(`${agent}Progress`);
            progressEl.style.width = '0%';
            
            // Reset time
            const timeEl = document.getElementById(`${agent}Time`);
            timeEl.textContent = '0.0s';
            
            // Clear result
            const resultEl = document.getElementById(`${agent}Result`);
            resultEl.innerHTML = '';
        });
    }

    displaySummary(results) {
        const summaryContent = document.getElementById('summaryContent');
        const qualityAssessment = results.quality_assessment || {};
        
        summaryContent.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-white mb-2">Task Overview</h4>
                    <p class="text-white/80">${this.currentTask}</p>
                </div>
                <div>
                    <h4 class="font-semibold text-white mb-2">Execution Time</h4>
                    <p class="text-white/80">${(results.total_time || 0).toFixed(2)} seconds</p>
                    ${results.agent_times ? `
                        <div class="mt-2 text-sm text-white/60">
                            <div>Research: ${results.agent_times.research?.toFixed(2) || 0}s</div>
                            <div>Planning: ${results.agent_times.planning?.toFixed(2) || 0}s</div>
                            <div>Coding: ${results.agent_times.coding?.toFixed(2) || 0}s</div>
                            <div>Execution: ${results.agent_times.execution?.toFixed(2) || 0}s</div>
                        </div>
                    ` : ''}
                </div>
                ${qualityAssessment.overall_score ? `
                    <div>
                        <h4 class="font-semibold text-white mb-2">Quality Assessment</h4>
                        <div class="flex items-center space-x-3">
                            <div class="text-2xl font-bold ${this.getQualityColor(qualityAssessment.overall_score)}">
                                ${qualityAssessment.overall_score}/100
                            </div>
                            <div class="text-sm text-white/60">
                                Grade: ${qualityAssessment.grade || 'N/A'}
                            </div>
                        </div>
                        ${qualityAssessment.assessment_details ? `
                            <div class="mt-2 text-sm text-white/60">
                                <div>Research: ${qualityAssessment.assessment_details.research || 'N/A'}</div>
                                <div>Planning: ${qualityAssessment.assessment_details.planning || 'N/A'}</div>
                                <div>Coding: ${qualityAssessment.assessment_details.coding || 'N/A'}</div>
                            </div>
                        ` : ''}
                    </div>
                ` : ''}
                <div>
                    <h4 class="font-semibold text-white mb-2">Agent Performance</h4>
                    <div class="grid grid-cols-2 gap-2 text-sm">
                        <div class="flex items-center">
                            <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                            Research: Completed
                        </div>
                        <div class="flex items-center">
                            <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                            Planning: Completed
                        </div>
                        <div class="flex items-center">
                            <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                            Coding: Completed
                        </div>
                        <div class="flex items-center">
                            <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                            Execution: Completed
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getQualityColor(score) {
        if (score >= 90) return 'text-green-400';
        if (score >= 80) return 'text-blue-400';
        if (score >= 70) return 'text-yellow-400';
        if (score >= 60) return 'text-orange-400';
        return 'text-red-400';
    }

    updateTabContents(results) {
        // Update research tab
        document.getElementById('researchContent').innerHTML = `
            <div class="prose prose-invert max-w-none">
                <p>${this.formatText(results.research || 'No research results available')}</p>
            </div>
        `;
        
        // Update planning tab
        document.getElementById('planningContent').innerHTML = `
            <div class="prose prose-invert max-w-none">
                <p>${this.formatText(results.plan || 'No planning results available')}</p>
            </div>
        `;
        
        // Update code tab
        let codeContent = '';
        if (typeof results.code === 'object' && results.code.code) {
            const language = this.getLanguageClass(results.code.language || 'text');
            codeContent = `
                <div class="mb-3">
                    <span class="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">${results.code.language || 'Unknown'}</span>
                    <span class="text-xs text-white/60 ml-2">${results.code.summary || 'Code generated successfully'}</span>
                </div>
                <div class="code-container">
                    <pre><code class="${language}">${this.escapeHtml(results.code.code)}</code></pre>
                </div>
            `;
        } else {
            codeContent = `
                <div class="code-container">
                    <pre><code class="language-text">${this.escapeHtml(results.code || 'No code results available')}</code></pre>
                </div>
            `;
        }
        
        document.getElementById('codeContent').innerHTML = codeContent;
        
        // Update execution tab
        document.getElementById('executionContent').innerHTML = `
            <div class="prose prose-invert max-w-none">
                <p>${this.formatText(results.execution || 'No execution results available')}</p>
            </div>
        `;
        
        // Re-highlight code
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        }
    }

    getLanguageClass(language) {
        const languageMap = {
            'python': 'language-python',
            'javascript': 'language-javascript',
            'js': 'language-javascript',
            'html': 'language-html',
            'css': 'language-css',
            'json': 'language-json'
        };
        return languageMap[language.toLowerCase()] || 'language-text';
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            if (btn.dataset.tab === tabName) {
                btn.classList.add('border-blue-500');
                btn.classList.remove('border-transparent');
            } else {
                btn.classList.remove('border-blue-500');
                btn.classList.add('border-transparent');
            }
        });
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}Tab`).classList.add('active');
    }

    copyCode() {
        if (!this.results || !this.results.code) return;
        
        const code = typeof this.results.code === 'object' ? this.results.code.code : this.results.code;
        
        navigator.clipboard.writeText(code).then(() => {
            this.showToast('Code copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy code:', err);
            this.showToast('Failed to copy code', 'error');
        });
    }

    downloadCode() {
        if (!this.results || !this.results.code) return;
        
        const code = typeof this.results.code === 'object' ? this.results.code.code : this.results.code;
        const language = typeof this.results.code === 'object' ? this.results.code.language : 'text';
        const filename = `generated_code.${this.getFileExtension(language)}`;
        
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast(`Downloaded ${filename}`);
    }

    getFileExtension(language) {
        const extensions = {
            'python': 'py',
            'javascript': 'js',
            'html': 'html',
            'css': 'css',
            'json': 'json'
        };
        return extensions[language.toLowerCase()] || 'txt';
    }

    async downloadProject() {
        if (!this.results) {
            this.showToast('No results to download', 'error');
            return;
        }
        
        try {
            const zip = new JSZip();
            
            // Add code file
            const code = typeof this.results.code === 'object' ? this.results.code.code : this.results.code;
            const language = typeof this.results.code === 'object' ? this.results.code.language : 'text';
            const filename = `generated_code.${this.getFileExtension(language)}`;
            zip.file(filename, code);
            
            // Add README
            const readme = this.generateReadme();
            zip.file('README.md', readme);
            
            // Add results as JSON
            zip.file('results.json', JSON.stringify(this.results, null, 2));
            
            // Generate and download zip
            const blob = await zip.generateAsync({ type: 'blob' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ai_agent_project.zip';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.showToast('Project downloaded successfully!');
            
        } catch (error) {
            console.error('Download failed:', error);
            this.showToast('Failed to download project', 'error');
        }
    }

    generateReadme() {
        return `# AI Multi-Agent System Generated Project

## Task
${this.currentTask}

## Generated Code
${typeof this.results.code === 'object' ? this.results.code.summary : 'Code generated successfully'}

## Results
- Research: ${this.results.research ? 'Completed' : 'N/A'}
- Planning: ${this.results.plan ? 'Completed' : 'N/A'}
- Coding: ${this.results.code ? 'Completed' : 'N/A'}
- Execution: ${this.results.execution ? 'Completed' : 'N/A'}

## Generated At
${new Date().toISOString()}

---
Generated by AI Multi-Agent System
`;
    }

    clearInput() {
        document.getElementById('taskInput').value = '';
        document.getElementById('taskInput').focus();
    }

    retryTask() {
        this.hideError();
        if (this.currentTask) {
            document.getElementById('taskInput').value = this.currentTask;
            this.handleSubmit();
        }
    }

    updateRunButton(isProcessing) {
        const btn = document.getElementById('runBtn');
        const icon = btn.querySelector('i');
        
        if (isProcessing) {
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Processing...';
            btn.classList.add('opacity-50', 'cursor-not-allowed');
        } else {
            btn.disabled = false;
            btn.innerHTML = '<i data-lucide="play" class="w-4 h-4 mr-2"></i>Run Agents';
            btn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
        
        // Re-initialize icons
        lucide.createIcons();
    }

    showResults() {
        document.getElementById('resultsSection').classList.remove('hidden');
        document.getElementById('resultsSection').classList.add('animate-fade-in');
    }

    hideResults() {
        document.getElementById('resultsSection').classList.add('hidden');
    }

    showError(message) {
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorSection.classList.remove('hidden');
        errorSection.classList.add('animate-fade-in');
    }

    hideError() {
        document.getElementById('errorSection').classList.add('hidden');
    }

    showToast(message, type = 'success') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `fixed top-20 right-4 px-4 py-3 rounded-lg glass-morphism text-white animate-slide-up z-50`;
        
        if (type === 'error') {
            toast.classList.add('bg-red-500/20');
        } else {
            toast.classList.add('bg-green-500/20');
        }
        
        toast.innerHTML = `
            <div class="flex items-center">
                <i data-lucide="${type === 'error' ? 'alert-circle' : 'check-circle'}" class="w-5 h-5 mr-2"></i>
                ${message}
            </div>
        `;
        
        document.body.appendChild(toast);
        lucide.createIcons();
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('animate-fade-out');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }

    logDebug(message, data = null) {
        const debugPanel = document.getElementById('debugPanel');
        const debugContent = document.getElementById('debugContent');
        
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = `[${timestamp}] ${message}`;
        
        if (data) {
            debugContent.innerHTML += `${logEntry}\n${JSON.stringify(data, null, 2)}\n\n`;
        } else {
            debugContent.innerHTML += `${logEntry}\n`;
        }
        
        // Auto-scroll to bottom
        debugContent.scrollTop = debugContent.scrollHeight;
        
        // Show debug panel (can be toggled with a key)
        if (debugPanel.classList.contains('hidden')) {
            // Uncomment to show debug panel by default
            // debugPanel.classList.remove('hidden');
        }
    }

    formatText(text) {
        if (!text) return '';
        return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AIMultiAgentSystem();
    
    // Load dark mode preference
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        window.app.toggleDarkMode();
    }
    
    // Debug: Toggle debug panel with Ctrl+Shift+D
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
            const debugPanel = document.getElementById('debugPanel');
            debugPanel.classList.toggle('hidden');
        }
    });
    
    console.log('🚀 AI Multi-Agent System initialized');
    console.log('🔧 Press Ctrl+Shift+D to toggle debug panel');
});
