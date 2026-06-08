import React, { useState, useEffect } from 'react';
import type { Project } from '../data/projectData';
import { Eye, Info, Share2, Award, ChevronDown, ChevronUp } from 'lucide-react';

interface ProjectDashboardProps {
  project: Project;
}

export const ProjectDashboard: React.FC<ProjectDashboardProps> = ({ project }) => {
  const [activeChartTab, setActiveChartTab] = useState<string>('');
  const [chartLoading, setChartLoading] = useState<boolean>(true);
  const [activeAccordion, setActiveAccordion] = useState<string>('insights'); // 'insights', 'specs', or ''

  // Reset chart tab to the first chart when switching projects
  useEffect(() => {
    if (project.charts && project.charts.length > 0) {
      setActiveChartTab(project.charts[0].id);
      setChartLoading(true);
    } else {
      setActiveChartTab('');
    }
  }, [project.id]);

  const activeChart = project.charts.find(c => c.id === activeChartTab);

  // Compute full asset path, taking into account Vite base path
  const getChartUrl = (filename: string) => {
    const baseUrl = import.meta.env.BASE_URL || '/';
    return `${baseUrl}projects/${project.id}/outputs/${filename}`;
  };

  const handleIframeLoad = () => {
    setChartLoading(false);
  };

  const handleChartTabChange = (chartId: string) => {
    if (chartId !== activeChartTab) {
      setActiveChartTab(chartId);
      setChartLoading(true);
    }
  };

  const toggleAccordion = (section: string) => {
    setActiveAccordion(activeAccordion === section ? '' : section);
  };

  return (
    <div className="project-dashboard transition-view" key={project.id}>
      {/* Project Header */}
      <header className="project-header card-glass glow-cyan">
        <div className="header-meta">
          <span className="project-badge">P{project.number.toString().padStart(2, '0')}</span>
          <span className="project-season">{project.season}</span>
        </div>
        <h1 className="project-title">{project.title}</h1>
        <div className="project-discipline">{project.discipline}</div>
        <p className="project-description">{project.description}</p>
      </header>

      {/* Metrics Row */}
      <section className="metrics-section">
        <h2 className="section-title">Telemetry & Model Metrics</h2>
        <div className="grid-cols-1-2-4">
          {project.metrics.map((metric, idx) => (
            <div key={idx} className="metric-box card-glass">
              <span className="metric-label">{metric.label}</span>
              <span className="metric-value">{metric.value}</span>
              {metric.subtext && <span className="metric-subtext">{metric.subtext}</span>}
            </div>
          ))}
        </div>
      </section>

      {/* Main Interactive Visualizer */}
      <section className="visualizer-section">
        <h2 className="section-title">Interactive Telemetry Plots</h2>
        <div className="visualizer-container card-glass">
          {/* Chart selector tabs */}
          <div className="chart-tabs">
            {project.charts.map((chart) => (
              <button
                key={chart.id}
                className={`chart-tab-btn ${activeChartTab === chart.id ? 'active' : ''}`}
                onClick={() => handleChartTabChange(chart.id)}
              >
                <Eye size={14} />
                <span>{chart.title}</span>
              </button>
            ))}
          </div>

          {/* Visualization Frame wrapper */}
          <div className="visualizer-frame-wrapper">
            {activeChart && (
              <>
                {chartLoading && (
                  <div className="chart-spinner-container">
                    <div className="chart-spinner"></div>
                    <p className="spinner-text">STREAMING HIGH-FREQUENCY TELEMETRY...</p>
                  </div>
                )}
                <iframe
                  src={getChartUrl(activeChart.filename)}
                  className={`visualizer-iframe ${chartLoading ? 'loading' : ''}`}
                  title={activeChart.title}
                  loading="lazy"
                  onLoad={handleIframeLoad}
                />
              </>
            )}
            {!activeChart && (
              <div className="no-chart-state">
                <Info size={32} />
                <p>No active visualizations selected</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Collapsible details sections */}
      <section className="details-accordion-section">
        {/* Accordion 1: Insights & LinkedIn */}
        <div className="accordion-item card-glass">
          <button 
            className="accordion-header" 
            onClick={() => toggleAccordion('insights')}
          >
            <div className="accordion-title-wrapper">
              <Share2 size={18} className="accordion-icon" style={{ color: 'var(--f1-red)' }} />
              <span>STRATEGIC CAMPAIGN INSIGHTS</span>
            </div>
            {activeAccordion === 'insights' ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>
          <div className={`accordion-content ${activeAccordion === 'insights' ? 'open' : ''}`}>
            <div className="insights-panel">
              <div className="linkedin-mockup">
                <div className="linkedin-header">
                  <div className="linkedin-avatar">LK</div>
                  <div className="linkedin-user">
                    <span className="user-name">Lalith Kaamala</span>
                    <span className="user-title">Formula 1 Data Scientist & Decision Engineer</span>
                  </div>
                </div>
                <div className="linkedin-body">
                  <p className="hook-text">{project.linkedinHook}</p>
                  <p className="body-text">{project.linkedinBody}</p>
                  <div className="visual-indicator">📸 [Interactive Dashboard Plotly Visuals Attached]</div>
                </div>
              </div>
              
              <div className="insights-summary-list">
                <h4 className="insights-list-title">Core Analytical Takeaways:</h4>
                <ul>
                  {project.insights.map((insight: any, idx: number) => (
                    <li key={idx}>
                      <span className="insight-bullet"></span>
                      <p>{insight.value}</p>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Accordion 2: Specs & Model Architecture */}
        <div className="accordion-item card-glass">
          <button 
            className="accordion-header" 
            onClick={() => toggleAccordion('specs')}
          >
            <div className="accordion-title-wrapper">
              <Award size={18} className="accordion-icon" style={{ color: 'var(--accent-cyan)' }} />
              <span>MODEL ARCHITECTURE & SPECIFICATIONS</span>
            </div>
            {activeAccordion === 'specs' ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>
          <div className={`accordion-content ${activeAccordion === 'specs' ? 'open' : ''}`}>
            <div className="specs-panel">
              <div className="specs-table-wrapper">
                <table className="specs-table">
                  <thead>
                    <tr>
                      <th>Parameters</th>
                      <th>Configuration / Target Engine</th>
                    </tr>
                  </thead>
                  <tbody>
                    {project.specifications.map((spec, idx) => (
                      <tr key={idx}>
                        <td className="spec-label-cell">{spec.label}</td>
                        <td className="spec-value-cell text-mono">{spec.value}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="specs-callout">
                <h4 className="callout-title">Workspace Reference</h4>
                <p>
                  The pipeline scripts, data collectors, and model training routines reside locally in:
                </p>
                <code className="workspace-path text-mono">f1-lab/projects/{project.id}/src/</code>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
