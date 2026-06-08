import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Overview } from './components/Overview';
import { ProjectDashboard } from './components/ProjectDashboard';
import { projectsData } from './data/projectData';

function App() {
  const [activeView, setActiveView] = useState<string>('overview');
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);

  const selectedProject = projectsData.find((p) => p.id === activeView);

  const handleSelectView = (view: string) => {
    setActiveView(view);
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        projects={projectsData}
        activeView={activeView}
        onSelectView={handleSelectView}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
      />

      {/* Main Viewport Content */}
      <main className="main-content">
        {activeView === 'overview' && (
          <Overview 
            projects={projectsData} 
            onSelectProject={handleSelectView} 
          />
        )}
        {selectedProject && (
          <ProjectDashboard 
            project={selectedProject} 
          />
        )}
      </main>
    </div>
  );
}

export default App;
