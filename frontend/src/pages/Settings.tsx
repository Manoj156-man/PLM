import { useState } from 'react'
import { Save, Sliders, Database, Bell, Shield, Key } from 'lucide-react'
import './Settings.css'

export default function Settings() {
  const [agents, setAgents] = useState({
    supervisor: true,
    design: true,
    manufacturing: false,
    quality: true
  })
  
  const [creativity, setCreativity] = useState(75)

  const handleToggle = (key: keyof typeof agents) => {
    setAgents(prev => ({ ...prev, [key]: !prev[key] }))
  }

  return (
    <div className="settings-container animate-fade-in">
      <header className="settings-header">
        <div>
          <h2 className="settings-title">System Settings</h2>
          <p className="settings-subtitle">Configure AI agents, integrations, and preferences</p>
        </div>
        <button className="btn btn-primary">
          <Save size={20} /> Save Configuration
        </button>
      </header>

      <div className="settings-grid">
        {/* Agent Configuration */}
        <section className="glass-panel settings-section">
          <h3 className="section-title text-blue">
            <Sliders size={24} /> AI Agent Configuration
          </h3>
          
          <div className="settings-group">
            <h4 className="group-title">Active Specialized Agents</h4>
            <div className="toggle-list">
              <label className="toggle-item">
                <div className="toggle-info">
                  <span className="toggle-label">Supervisor Agent</span>
                  <span className="toggle-desc">Coordinates tasks and product state transitions.</span>
                </div>
                <div className={`custom-toggle ${agents.supervisor ? 'active' : ''}`} onClick={() => handleToggle('supervisor')}>
                  <div className="toggle-knob"></div>
                </div>
              </label>

              <label className="toggle-item">
                <div className="toggle-info">
                  <span className="toggle-label">Design Agent</span>
                  <span className="toggle-desc">Generates CAD files and design documentation.</span>
                </div>
                <div className={`custom-toggle ${agents.design ? 'active' : ''}`} onClick={() => handleToggle('design')}>
                  <div className="toggle-knob"></div>
                </div>
              </label>

              <label className="toggle-item">
                <div className="toggle-info">
                  <span className="toggle-label">Manufacturing Agent</span>
                  <span className="toggle-desc">Analyzes supply chain and production lines.</span>
                </div>
                <div className={`custom-toggle ${agents.manufacturing ? 'active' : ''}`} onClick={() => handleToggle('manufacturing')}>
                  <div className="toggle-knob"></div>
                </div>
              </label>

              <label className="toggle-item">
                <div className="toggle-info">
                  <span className="toggle-label">Quality Control Agent</span>
                  <span className="toggle-desc">Simulates structural testing and anomaly detection.</span>
                </div>
                <div className={`custom-toggle ${agents.quality ? 'active' : ''}`} onClick={() => handleToggle('quality')}>
                  <div className="toggle-knob"></div>
                </div>
              </label>
            </div>
          </div>

          <div className="settings-group">
            <div className="flex-between">
              <h4 className="group-title mb-0">Global AI Creativity Level</h4>
              <span className="creativity-value">{creativity}%</span>
            </div>
            <p className="toggle-desc mb-4">Adjust the balance between deterministic precision and creative problem solving.</p>
            <input 
              type="range" 
              className="custom-slider" 
              min="0" max="100" 
              value={creativity}
              onChange={(e) => setCreativity(Number(e.target.value))}
            />
            <div className="slider-labels">
              <span>Precision</span>
              <span>Creativity</span>
            </div>
          </div>
        </section>

        <div className="settings-column">
          {/* Integrations */}
          <section className="glass-panel settings-section">
            <h3 className="section-title text-magenta">
              <Database size={24} /> External Integrations
            </h3>
            
            <div className="settings-group">
              <label className="input-group">
                <span className="input-label flex-align"><Key size={16}/> OpenAI API Key</span>
                <input type="password" placeholder="sk-..." className="input-field w-full" defaultValue="sk-dummy-key-for-demo-purposes" />
              </label>
              
              <label className="input-group mt-4">
                <span className="input-label flex-align"><Database size={16}/> Main Database URI</span>
                <input type="text" placeholder="postgresql://..." className="input-field w-full" defaultValue="postgresql://postgres:password@localhost:5432/plm" />
              </label>
            </div>
          </section>

          {/* System Preferences */}
          <section className="glass-panel settings-section mt-6">
            <h3 className="section-title text-emerald">
              <Shield size={24} /> System Preferences
            </h3>
            
            <div className="toggle-list">
              <label className="toggle-item">
                <div className="flex-align" style={{ gap: '16px' }}>
                  <Bell size={20} className="text-muted"/>
                  <div className="toggle-info">
                    <span className="toggle-label">Push Notifications</span>
                    <span className="toggle-desc">Receive alerts for critical agent failures.</span>
                  </div>
                </div>
                <div className="custom-toggle active">
                  <div className="toggle-knob"></div>
                </div>
              </label>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
