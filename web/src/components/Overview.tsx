import React from 'react';
import { type Project, statistics, timelineEvents } from '../data/projectData';
import { Play, TrendingUp, Cpu, Award } from 'lucide-react';

interface OverviewProps {
  projects: Project[];
  onSelectProject: (id: string) => void;
}

export const Overview: React.FC<OverviewProps> = ({ projects, onSelectProject }) => {
  // Helpers to assign icons to stats
  const getStatIcon = (label: string) => {
    if (label.includes('Project')) return <Award className="stat-icon" size={24} style={{ color: 'var(--f1-red)' }} />;
    if (label.includes('Season')) return <TrendingUp className="stat-icon" size={24} style={{ color: 'var(--accent-cyan)' }} />;
    if (label.includes('Models')) return <Cpu className="stat-icon" size={24} style={{ color: 'var(--accent-green)' }} />;
    return <Play className="stat-icon" size={24} style={{ color: 'var(--accent-yellow)' }} />;
  };

  return (
    <div className="overview-container transition-view">
      {/* Welcome Banner */}
      <div className="overview-hero card-glass glow-red">
        <div className="hero-badge">OFFICIAL PORTAL</div>
        <h1 className="hero-title">F1 ENGINEERING & DECISION SCIENCE HUB</h1>
        <p className="hero-subtitle">
          An interactive telemetry platform exploring Formula 1 race dynamics, tire degradation, 
          grid prediction, and operational strategy using Machine Learning, Monte Carlo Simulations, 
          Game Theory, and Deep Reinforcement Learning.
        </p>
      </div>

      {/* Stats Summary Grid */}
      <section className="stats-section">
        <h2 className="section-title">SYSTEM TELEMETRY SUMMARY</h2>
        <div className="grid-cols-1-2-4">
          {statistics.map((stat, idx) => (
            <div key={idx} className="stat-card card-glass">
              <div className="stat-header">
                <span className="stat-label">{stat.label}</span>
                {getStatIcon(stat.label)}
              </div>
              <div className="stat-value">{stat.value}</div>
              <div className="stat-change">{stat.change}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Projects Grid */}
      <section className="projects-section">
        <h2 className="section-title">COMPLETED PROJECTS</h2>
        <div className="project-grid">
          {projects.map((project) => (
            <div 
              key={project.id} 
              className="project-card card-glass"
              onClick={() => onSelectProject(project.id)}
            >
              <div className="project-card-header">
                <span className="project-num">PROJECT {project.number.toString().padStart(2, '0')}</span>
                <span className="project-season-badge">{project.season}</span>
              </div>
              <h3 className="project-card-title">{project.title}</h3>
              <div className="project-discipline-badge">{project.discipline}</div>
              <p className="project-card-desc">{project.description}</p>
              
              <div className="project-card-footer">
                <span className="launch-link">
                  Launch telemetry <span>→</span>
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Timeline Section */}
      <section className="timeline-section">
        <h2 className="section-title">SERIES DEPLOYMENT CHRONOLOGY</h2>
        <div className="timeline-container card-glass">
          <div className="timeline-line"></div>
          <div className="timeline-events">
            {timelineEvents.map((evt, idx) => (
              <div key={idx} className="timeline-item">
                <div className="timeline-marker">
                  <span className="marker-dot"></span>
                  <span className="marker-num">{evt.round}</span>
                </div>
                <div className="timeline-content">
                  <span className="timeline-date">{evt.date}</span>
                  <h3 className="timeline-event-title">{evt.title}</h3>
                  <p className="timeline-event-desc">{evt.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
