import { Outlet, NavLink } from 'react-router-dom'
import { Activity, LayoutDashboard, Settings } from 'lucide-react'
import './Layout.css' // We will create this

export default function Layout() {
  return (
    <div className="app-container">
      <aside className="sidebar glass-panel">
        <div className="sidebar-header">
          <h1 className="logo text-gradient">
            <Activity className="logo-icon" /> PLM<span className="logo-light">AI</span>
          </h1>
        </div>
        <nav className="sidebar-nav">
          <NavLink 
            to="/" 
            end
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
          </NavLink>
          <NavLink 
            to="/settings"
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <Settings size={20} />
            <span>Settings</span>
          </NavLink>
        </nav>
        <div className="sidebar-footer">
          Agentic AI Engine v2.0
        </div>
      </aside>
      
      <main className="main-content">
        <div className="content-wrapper">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
