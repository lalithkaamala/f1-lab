import React from 'react';
import { 
  LayoutDashboard, 
  BarChart3, 
  TrendingUp, 
  Compass, 
  Shuffle, 
  Target, 
  Activity, 
  Cpu, 
  Terminal,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import type { Project } from '../data/projectData';

interface SidebarProps {
  projects: Project[];
  activeView: string;
  onSelectView: (view: string) => void;
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  projects,
  activeView,
  onSelectView,
  collapsed,
  setCollapsed
}) => {
  // Mapping project numbers to Lucide icons
  const getIcon = (num: number) => {
    switch (num) {
      case 1: return <BarChart3 size={20} />;
      case 2: return <TrendingUp size={20} />;
      case 3: return <Compass size={20} />;
      case 4: return <Shuffle size={20} />;
      case 5: return <Target size={20} />;
      case 6: return <Activity size={20} />;
      case 7: return <Cpu size={20} />;
      case 8: return <Terminal size={20} />;
      default: return <BarChart3 size={20} />;
    }
  };

  return (
    <aside className={`sidebar-container ${collapsed ? 'collapsed' : ''}`}>
      {/* Header section */}
      <div className="sidebar-header">
        {!collapsed && (
          <div className="logo-area">
            <span className="logo-f1">F1</span>
            <span className="logo-lab">LAB</span>
          </div>
        )}
        {collapsed && (
          <div className="logo-area-collapsed">🏁</div>
        )}
        <button 
          className="collapse-btn" 
          onClick={() => setCollapsed(!collapsed)}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Connection status */}
      <div className="pit-connection">
        <div className={`status-dot ${collapsed ? '' : 'pulse'}`}></div>
        {!collapsed && <span className="status-text">PIT LINK: ACTIVE</span>}
      </div>

      {/* Navigation menu */}
      <nav className="sidebar-nav">
        <div className="nav-section-label">{collapsed ? '•' : 'MAIN MENU'}</div>
        <button
          className={`nav-item ${activeView === 'overview' ? 'active' : ''}`}
          onClick={() => onSelectView('overview')}
        >
          <LayoutDashboard size={20} />
          {!collapsed && <span>Overview Dashboard</span>}
        </button>

        <div className="nav-section-label">{collapsed ? '•' : 'F1 PROJECTS'}</div>
        <div className="projects-list">
          {projects.map((project) => {
            const isActive = activeView === project.id;
            return (
              <button
                key={project.id}
                className={`nav-item project-nav-item ${isActive ? 'active' : ''}`}
                onClick={() => onSelectView(project.id)}
                title={project.title}
              >
                <div className="nav-icon-wrapper">
                  {getIcon(project.number)}
                  {isActive && <div className="active-dot" />}
                </div>
                {!collapsed && (
                  <div className="project-details">
                    <span className="project-title-nav">P{project.number}: {project.title}</span>
                    <span className="project-desc-nav">{project.discipline}</span>
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </nav>

      {/* Sidebar Footer */}
      <div className="sidebar-footer">
        {!collapsed && (
          <div className="footer-credits">
            <p className="credits-title">F1 LAB PORTAL</p>
            <p className="credits-author">by Lalith Kaamala</p>
          </div>
        )}
      </div>
    </aside>
  );
};
