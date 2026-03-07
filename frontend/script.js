// AI Multi-Agent System - Frontend JavaScript

class AIMultiAgentSystem {
    constructor() {
        this.apiBase = "http://127.0.0.1:8002";
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
            const response = await fetch(`${this.apiBase}/process-task`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
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
        // Display results for each agent using simplified format
        await this.displaySimpleAgentResult('research', results.research);
        await this.displaySimpleAgentResult('planning', results.plan);
        await this.displayCodeResult(results.code);  // Special handling for code
        await this.displaySimpleAgentResult('execution', results.execution);
        
        // Display summary
        this.displaySimpleSummary(results);
        
        // Display detailed results in tabs
        this.displaySimpleDetailedResults(results);
    }

    async displayCodeResult(codeData) {
        if (!codeData) return;
        
        const card = document.getElementById('codingAgent');
        const status = card.querySelector('.agent-status');
        const progress = document.getElementById('codingProgress');
        const resultDiv = document.getElementById('codingResult');
        
        // Update status to processing
        status.textContent = 'Processing';
        status.className = 'agent-status processing';
        card.classList.add('active');
        
        // Animate progress
        await this.animateProgress(progress, 100);
        
        // Update to completed
        status.textContent = 'Completed';
        status.className = 'agent-status completed';
        
        // Handle different code data formats
        let codeContent = '';
        let language = 'text';
        
        if (typeof codeData === 'object' && codeData.code) {
            // Structured code data
            language = codeData.language || 'text';
            codeContent = `
                <div class="code-header">
                    <h4><strong>Language:</strong> ${codeData.language || 'Unknown'}</h4>
                    <p><strong>Summary:</strong> ${codeData.summary || 'Code generated successfully'}</p>
                </div>
                <div class="code-block">
                    <pre><code class="language-${language}">${this.escapeHtml(codeData.code)}</code></pre>
                </div>
            `;
        } else {
            // Simple string code
            codeContent = `
                <div class="code-block">
                    <pre><code class="language-text">${this.escapeHtml(codeData)}</code></pre>
                </div>
            `;
        }
        
        // Display result
        resultDiv.innerHTML = `
            <p><strong>Status:</strong> ${status.textContent}</p>
            ${codeContent}
        `;
        
        // Add completion class
        setTimeout(() => {
            card.classList.add('completed');
        }, 500);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async displaySimpleAgentResult(agentType, result) {
        if (!result) return;
        
        const card = document.getElementById(`${agentType}Agent`);
        const status = card.querySelector('.agent-status');
        const progress = document.getElementById(`${agentType}Progress`);
        const resultDiv = document.getElementById(`${agentType}Result`);
        
        // Update status
        status.textContent = 'Completed';
        status.className = 'agent-status completed';
        
        // Animate progress
        await this.animateProgress(progress, 100);
        
        // Display result summary
        resultDiv.innerHTML = `<p><strong>Status:</strong> ${status.textContent}</p><p>${result}</p>`;
        
        // Add completion class after animation
        setTimeout(() => {
            card.classList.add('completed');
        }, 500);
    }

    displaySimpleSummary(results) {
        const summaryContent = document.getElementById('summaryContent');
        
        const summaryHTML = `
            <div class="summary-card">
                <h3>Task Summary</h3>
                <p><strong>Original Task:</strong> ${this.currentTask}</p>
                <p><strong>Processing Time:</strong> ${results.total_time ? `${results.total_time.toFixed(2)}s` : 'N/A'}</p>
                
                <h4>Agent Results</h4>
                <ul>
                    <li><strong>Research:</strong> ${results.research || 'Completed'}</li>
                    <li><strong>Planning:</strong> ${results.plan || 'Completed'}</li>
                    <li><strong>Coding:</strong> ${results.code || 'Completed'}</li>
                    <li><strong>Execution:</strong> ${results.execution || 'Completed'}</li>
                </ul>
                
                <h4>Final Output</h4>
                <div class="final-output">
                    ${this.formatText(results.execution || 'No final output available')}
                </div>
            </div>
        `;
        
        summaryContent.innerHTML = summaryHTML;
    }

    displaySimpleDetailedResults(results) {
        // Update all tabs with simplified results
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
        
        // Special handling for code tab
        let codeContent = '';
        if (typeof results.code === 'object' && results.code.code) {
            codeContent = `
                <div class="code-header">
                    <h4><strong>Language:</strong> ${results.code.language || 'Unknown'}</h4>
                    <p><strong>Summary:</strong> ${results.code.summary || 'Code generated successfully'}</p>
                </div>
                <div class="code-block">
                    <pre><code class="language-${results.code.language || 'text'}">${this.escapeHtml(results.code.code)}</code></pre>
                </div>
            `;
        } else {
            codeContent = `
                <div class="code-block">
                    <pre><code class="language-text">${this.escapeHtml(results.code || 'No code results available')}</code></pre>
                </div>
            `;
        }
        
        document.getElementById('codeContent').innerHTML = `
            <h3>Code Results</h3>
            <div class="detail-section">
                ${codeContent}
            </div>
        `;
        
        document.getElementById('finalContent').innerHTML = `
            <h3>Final Output</h3>
            <div class="detail-section">
                <p>${this.formatText(results.execution || 'No final output available')}</p>
            </div>
        `;
    }

    async displayAgentResult(agentType, result) {
        if (!result) return;
        
        const card = document.getElementById(`${agentType}Agent`);
        const status = card.querySelector('.agent-status');
        const progress = document.getElementById(`${agentType}Progress`);
        const resultDiv = document.getElementById(`${agentType}Result`);
        
        // Update status
        status.textContent = 'Completed';
        status.className = 'agent-status completed';
        
        // Animate progress
        await this.animateProgress(progress, 100);
        
        // Display result summary
        let summary = '';
        if (agentType === 'research') {
            summary = result.result?.summary || 'Research completed';
        } else if (agentType === 'planning') {
            summary = result.result?.project_overview || 'Planning completed';
        } else if (agentType === 'coding') {
            summary = result.result?.implementation_summary || 'Coding completed';
        } else if (agentType === 'execution') {
            summary = result.result?.executive_summary || 'Execution completed';
        }
        
        resultDiv.innerHTML = `<p><strong>Status:</strong> ${status.textContent}</p><p>${summary}</p>`;
        
        // Add completion class after animation
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
                <p><strong>Original Task:</strong> ${results.task}</p>
                <p><strong>Processing Time:</strong> ${results.total_time ? `${results.total_time.toFixed(2)}s` : 'N/A'}</p>
                
                <h4>Agent Results</h4>
                <ul>
                    <li><strong>Research:</strong> ${results.research_result?.result?.summary || 'Completed'}</li>
                    <li><strong>Planning:</strong> ${results.planning_result?.result?.project_overview || 'Completed'}</li>
                    <li><strong>Coding:</strong> ${results.coding_result?.result?.implementation_summary || 'Completed'}</li>
                    <li><strong>Execution:</strong> ${results.execution_result?.result?.executive_summary || 'Completed'}</li>
                </ul>
                
                <h4>Final Output</h4>
                <div class="final-output">
                    ${this.formatText(results.final_output || 'No final output available')}
                </div>
            </div>
        `;
        
        summaryContent.innerHTML = summaryHTML;
    }

    displayDetailedResults(results) {
        // Research tab
        const researchContent = document.getElementById('researchContent');
        if (results.research_result?.result) {
            researchContent.innerHTML = this.formatResearchResult(results.research_result.result);
        }
        
        // Planning tab
        const planningContent = document.getElementById('planningContent');
        if (results.planning_result?.result) {
            planningContent.innerHTML = this.formatPlanningResult(results.planning_result.result);
        }
        
        // Code tab
        const codeContent = document.getElementById('codeContent');
        if (results.coding_result?.result) {
            codeContent.innerHTML = this.formatCodeResult(results.coding_result.result);
        }
        
        // Final tab
        const finalContent = document.getElementById('finalContent');
        if (results.execution_result?.result) {
            finalContent.innerHTML = this.formatFinalResult(results.execution_result.result);
        }
    }

    formatResearchResult(result) {
        return `
            <div class="research-details">
                <h3>Research Results</h3>
                
                <div class="detail-section">
                    <h4>Summary</h4>
                    <p>${this.formatText(result.summary || 'No summary available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Background</h4>
                    <p>${this.formatText(result.background || 'No background information available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Key Concepts</h4>
                    <ul>
                        ${(result.key_concepts || []).map(concept => `<li>${this.formatText(concept)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Requirements</h4>
                    <ul>
                        ${(result.requirements || []).map(req => `<li>${this.formatText(req)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Best Practices</h4>
                    <ul>
                        ${(result.best_practices || []).map(practice => `<li>${this.formatText(practice)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Resources</h4>
                    <ul>
                        ${(result.resources || []).map(resource => 
                            `<li><strong>${resource.name || 'Resource'}</strong> (${resource.type || 'unknown'}): ${resource.description || 'No description'}</li>`
                        ).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Complexity Assessment</h4>
                    <p><strong>Complexity:</strong> ${result.complexity_assessment || 'N/A'}</p>
                    <p><strong>Estimated Effort:</strong> ${result.estimated_effort || 'N/A'}</p>
                </div>
            </div>
        `;
    }

    formatPlanningResult(result) {
        return `
            <div class="planning-details">
                <h3>Planning Results</h3>
                
                <div class="detail-section">
                    <h4>Project Overview</h4>
                    <p>${this.formatText(result.project_overview || 'No overview available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Technical Approach</h4>
                    <p>${this.formatText(result.technical_approach || 'No technical approach specified')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Execution Steps</h4>
                    ${(result.steps || []).map((step, index) => `
                        <div class="step-card">
                            <h5>Step ${step.step_number || index + 1}: ${step.title || 'Untitled Step'}</h5>
                            <p>${this.formatText(step.description || 'No description')}</p>
                            <p><strong>Estimated Effort:</strong> ${step.estimated_effort || 'N/A'}</p>
                            ${(step.deliverables && step.deliverables.length > 0) ? 
                                `<p><strong>Deliverables:</strong></p><ul>${step.deliverables.map(d => `<li>${d}</li>`).join('')}</ul>` : ''
                            }
                        </div>
                    `).join('')}
                </div>
                
                <div class="detail-section">
                    <h4>Resource Requirements</h4>
                    <ul>
                        ${(result.resource_requirements || []).map(resource => 
                            `<li><strong>${resource.name || 'Resource'}</strong> (${resource.type || 'unknown'}): ${resource.purpose || 'No purpose specified'}</li>`
                        ).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Timeline & Duration</h4>
                    <p><strong>Estimated Duration:</strong> ${result.estimated_duration || 'N/A'}</p>
                    <p><strong>Timeline:</strong> ${result.timeline || 'N/A'}</p>
                </div>
            </div>
        `;
    }

    formatCodeResult(result) {
        return `
            <div class="code-details">
                <h3>Code Implementation</h3>
                
                <div class="detail-section">
                    <h4>Implementation Summary</h4>
                    <p>${this.formatText(result.implementation_summary || 'No summary available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Technical Details</h4>
                    <p><strong>Primary Language:</strong> ${result.primary_language || 'N/A'}</p>
                    <p><strong>Frameworks Used:</strong> ${(result.frameworks_used || []).join(', ') || 'None'}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Dependencies</h4>
                    <ul>
                        ${(result.dependencies || []).map(dep => 
                            `<li><strong>${dep.name || 'Dependency'}</strong> ${dep.version || ''} - ${dep.purpose || 'No purpose specified'}</li>`
                        ).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Generated Files</h4>
                    ${(result.files || []).map(file => `
                        <div class="file-card">
                            <h5><i class="fas fa-file-code"></i> ${file.file_path || 'Untitled File'}</h5>
                            <p><strong>Type:</strong> ${file.file_type || 'unknown'}</p>
                            <p><strong>Description:</strong> ${file.description || 'No description'}</p>
                            <div class="code-block">
                                <button class="copy-btn" onclick="copyToClipboard(this)">
                                    <i class="fas fa-copy"></i> Copy
                                </button>
                                <pre><code>${this.escapeHtml(file.content || 'No content')}</code></pre>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="detail-section">
                    <h4>Setup Instructions</h4>
                    <p>${this.formatText(result.setup_instructions || 'No setup instructions available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Usage Examples</h4>
                    <ul>
                        ${(result.usage_examples || []).map(example => `<li>${this.formatText(example)}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    formatFinalResult(result) {
        return `
            <div class="final-details">
                <h3>Final Execution Results</h3>
                
                <div class="detail-section">
                    <h4>Executive Summary</h4>
                    <p>${this.formatText(result.executive_summary || 'No executive summary available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Solution Overview</h4>
                    <p>${this.formatText(result.solution_overview || 'No solution overview available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Key Findings</h4>
                    <ul>
                        ${(result.key_findings || []).map(finding => `<li>${this.formatText(finding)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Implementation Summary</h4>
                    <p>${this.formatText(result.implementation_summary || 'No implementation summary available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Deliverables</h4>
                    <ul>
                        ${(result.deliverables || []).map(deliverable => 
                            `<li><strong>${deliverable.name || 'Deliverable'}</strong> (${deliverable.type || 'unknown'}): ${deliverable.description || 'No description'}</li>`
                        ).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Usage Instructions</h4>
                    <p>${this.formatText(result.usage_instructions || 'No usage instructions available')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>Benefits & Features</h4>
                    <ul>
                        ${(result.benefits_features || []).map(feature => `<li>${this.formatText(feature)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Limitations</h4>
                    <ul>
                        ${(result.limitations || []).map(limitation => `<li>${this.formatText(limitation)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Future Enhancements</h4>
                    <ul>
                        ${(result.future_enhancements || []).map(enhancement => `<li>${this.formatText(enhancement)}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h4>Complete Final Output</h4>
                    <div class="final-output">
                        ${this.formatText(result.final_output || 'No final output available')}
                    </div>
                </div>
            </div>
        `;
    }

    formatText(text) {
        if (!text) return '';
        // Convert newlines to HTML paragraphs
        return text.split('\n').map(line => line.trim() ? `<p>${line}</p>` : '').join('');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
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
                <p>The AI Multi-Agent System is a sophisticated platform where multiple intelligent AI agents collaborate to solve complex tasks through a structured workflow.</p>
                
                <h4>How It Works</h4>
                <ol>
                    <li><strong>Research Agent:</strong> Gathers and organizes information about your task</li>
                    <li><strong>Planning Agent:</strong> Creates a detailed step-by-step execution plan</li>
                    <li><strong>Coding Agent:</strong> Generates technical solutions and code</li>
                    <li><strong>Execution Agent:</strong> Synthesizes all results into a comprehensive final output</li>
                </ol>
                
                <h4>Technology Stack</h4>
                <ul>
                    <li>Backend: Python with FastAPI</li>
                    <li>AI Framework: LangChain with OpenAI</li>
                    <li>Frontend: Modern HTML, CSS, and JavaScript</li>
                </ul>
                
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
                    <li>"Design a database schema for an e-commerce platform"</li>
                </ul>
                
                <h4>Understanding Results</h4>
                <p>After processing, you can explore detailed results from each agent using the tabs:</p>
                <ul>
                    <li><strong>Summary:</strong> Overview of all results</li>
                    <li><strong>Research:</strong> Detailed research findings</li>
                    <li><strong>Planning:</strong> Execution plan and steps</li>
                    <li><strong>Code:</strong> Generated code and technical solutions</li>
                    <li><strong>Final Output:</strong> Comprehensive final result</li>
                </ul>
                
                <h4>Tips</h4>
                <ul>
                    <li>Be specific in your task description for better results</li>
                    <li>Use Ctrl+Enter to quickly submit your task</li>
                    <li>Check the agent progress cards to see real-time status</li>
                    <li>Copy code snippets using the copy button in code blocks</li>
                </ul>
            </div>
        `);
    }

    clearInput() {
        document.getElementById('taskInput').value = '';
        document.getElementById('submitBtn').disabled = true;
    }
}

// Utility function for copying code to clipboard
function copyToClipboard(button) {
    const codeBlock = button.parentElement.querySelector('code');
    const text = codeBlock.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.style.backgroundColor = 'var(--success-color)';
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.style.backgroundColor = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
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
