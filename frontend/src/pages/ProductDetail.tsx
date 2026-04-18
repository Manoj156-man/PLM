import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Play, AlertTriangle, CheckCircle2, Clock, GitCommit } from 'lucide-react'
import { apiClient, ProductDetail as ProductDetailType } from '../api/client'
import './ProductDetail.css'

const PHASES = [
  'ideation', 'design', 'manufacturing', 'quality_control',
  'inventory', 'sales', 'maintenance', 'end_of_life'
]

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>()
  const [product, setProduct] = useState<ProductDetailType | null>(null)
  const [loading, setLoading] = useState(true)
  const [agentRunning, setAgentRunning] = useState(false)

  const fetchProduct = async () => {
    try {
      const { data } = await apiClient.get<ProductDetailType>(`/products/${id}`)
      setProduct(data)
    } catch (error) {
      console.error("Failed to fetch product details", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProduct()
  }, [id])

  const triggerAgent = async () => {
    if (!product) return
    setAgentRunning(true)
    try {
      await apiClient.post(`/agents/trigger/${product.id}`)
      await fetchProduct()
    } catch (error) {
      console.error("Agent execution failed", error)
    } finally {
      setAgentRunning(false)
    }
  }

  if (loading) return (
    <div className="loading-state">
      <div className="spinner"></div>
    </div>
  )
  
  if (!product) return <div className="empty-state glass-panel">Product not found</div>

  const currentPhaseIndex = PHASES.indexOf(product.current_phase)

  return (
    <div className="product-detail-container animate-fade-in">
      <header className="detail-header">
        <div className="header-content">
          <Link to="/" className="back-link">
            <ArrowLeft size={16} /> Back to Dashboard
          </Link>
          <div className="title-row">
            <h2 className="detail-title">{product.name}</h2>
            <span className={`badge badge-${product.status}`}>
              {product.status}
            </span>
          </div>
          <p className="detail-description">{product.description}</p>
        </div>
        
        <button 
          onClick={triggerAgent} 
          disabled={agentRunning || product.status === 'completed'}
          className={`btn-trigger ${agentRunning || product.status === 'completed' ? 'disabled' : ''}`}
        >
          {agentRunning ? (
            <><div className="spinner-small"></div> Processing...</>
          ) : (
            <><Play size={20} fill="currentColor" /> Trigger AI Agent</>
          )}
        </button>
      </header>

      {/* Lifecycle Timeline UI */}
      <section className="glass-panel timeline-section">
        <h3 className="section-title">Lifecycle Progress</h3>
        <div className="timeline-container">
          <div className="timeline-track"></div>
          <div 
            className="timeline-progress"
            style={{ width: `${(currentPhaseIndex / (PHASES.length - 1)) * 100}%` }}
          ></div>
          
          {PHASES.map((phase, idx) => {
            const isCompleted = idx < currentPhaseIndex
            const isCurrent = idx === currentPhaseIndex
            
            let nodeClass = 'timeline-node'
            if (isCompleted) nodeClass += ' completed'
            if (isCurrent) nodeClass += ' current'
            
            return (
              <div key={phase} className="timeline-item">
                <div className={nodeClass}>
                  {isCompleted ? <CheckCircle2 size={24} /> : 
                   isCurrent ? <div className="node-pulse"></div> : 
                   <div className="node-dot"></div>}
                </div>
                <span className={`timeline-label ${isCurrent ? 'active' : ''}`}>
                  {phase.replace('_', ' ')}
                </span>
              </div>
            )
          })}
        </div>
      </section>

      <div className="detail-grid">
        {/* Events Log */}
        <section className="glass-panel events-section">
          <h3 className="section-title">
            <GitCommit className="icon-blue" /> Event Audit Log
          </h3>
          <div className="events-list custom-scrollbar">
            {product.events?.slice().reverse().map((event) => (
              <div key={event.id} className="event-item">
                <div className="event-marker"></div>
                <div className="event-header">
                  <span className="agent-id">{event.agent_id}</span>
                  <span className="event-type">{event.event_type}</span>
                  <span className="event-time">
                    <Clock size={12} /> {new Date(event.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <p className="event-description">{event.description}</p>
                <div className="event-phase">Phase: {event.phase.replace('_', ' ')}</div>
              </div>
            ))}
            {(!product.events || product.events.length === 0) && (
              <p className="empty-text">No events recorded yet.</p>
            )}
          </div>
        </section>

        <div className="side-sections">
          {/* Alerts */}
          <section className="glass-panel alerts-section">
            <div className="alert-glow"></div>
            <h3 className="section-title text-magenta">
              <AlertTriangle /> Active Alerts
            </h3>
            <div className="alerts-list">
              {product.alerts?.filter(a => !a.resolved).map(alert => (
                <div key={alert.id} className="alert-card">
                  <AlertTriangle className="alert-icon" size={24} />
                  <div>
                    <p className="alert-message">{alert.message}</p>
                    <p className="alert-meta">{alert.severity} • {new Date(alert.created_at).toLocaleString()}</p>
                  </div>
                </div>
              ))}
              {(!product.alerts || product.alerts.filter(a => !a.resolved).length === 0) && (
                <p className="empty-text">System operating normally. No active alerts.</p>
              )}
            </div>
          </section>

          {/* Tasks */}
          <section className="glass-panel tasks-section">
            <h3 className="section-title text-emerald">
              <CheckCircle2 /> Pending Tasks
            </h3>
            <div className="tasks-list">
              {product.tasks?.map(task => (
                <div key={task.id} className="task-card">
                  <div className="task-header">
                    <h4 className="task-title">{task.title}</h4>
                    <span className={`task-status ${task.status}`}>{task.status}</span>
                  </div>
                  <p className="task-description">{task.description}</p>
                  <p className="task-assignee">Assigned to: <span>{task.assigned_to_agent}</span></p>
                </div>
              ))}
              {(!product.tasks || product.tasks.length === 0) && (
                <p className="empty-text">No tasks generated yet.</p>
              )}
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
