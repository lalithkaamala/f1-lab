import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '..');
const projectsDir = path.join(rootDir, 'projects');
const publicDir = path.join(__dirname, 'public', 'projects');

// Ensure public/projects exists
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

const projects = fs.readdirSync(projectsDir).filter(f => {
  return fs.statSync(path.join(projectsDir, f)).isDirectory();
});

console.log(`Found projects: ${projects.join(', ')}`);

projects.forEach(project => {
  const projectSrcPath = path.join(projectsDir, project);
  const projectDestPath = path.join(publicDir, project);

  // Sync outputs (.html files)
  const outputsSrcDir = path.join(projectSrcPath, 'outputs');
  if (fs.existsSync(outputsSrcDir)) {
    const outputsDestDir = path.join(projectDestPath, 'outputs');
    fs.mkdirSync(outputsDestDir, { recursive: true });
    
    const files = fs.readdirSync(outputsSrcDir).filter(f => f.endsWith('.html'));
    files.forEach(file => {
      fs.copyFileSync(path.join(outputsSrcDir, file), path.join(outputsDestDir, file));
      console.log(`Copied: ${project}/outputs/${file}`);
    });
  }

  // Sync models (.json and .csv files)
  const modelsSrcDir = path.join(projectSrcPath, 'models');
  if (fs.existsSync(modelsSrcDir)) {
    const modelsDestDir = path.join(projectDestPath, 'models');
    fs.mkdirSync(modelsDestDir, { recursive: true });
    
    const files = fs.readdirSync(modelsSrcDir).filter(f => f.endsWith('.json') || f.endsWith('.csv'));
    files.forEach(file => {
      fs.copyFileSync(path.join(modelsSrcDir, file), path.join(modelsDestDir, file));
      console.log(`Copied: ${project}/models/${file}`);
    });
  }
});

// Sync processed data CSVs and JSONs from /data/processed
const processedDataSrcDir = path.join(rootDir, 'data', 'processed');
const processedDataDestDir = path.join(__dirname, 'public', 'data');
if (fs.existsSync(processedDataSrcDir)) {
  fs.mkdirSync(processedDataDestDir, { recursive: true });
  const files = fs.readdirSync(processedDataSrcDir).filter(f => f.endsWith('.csv') || f.endsWith('.json'));
  files.forEach(file => {
    fs.copyFileSync(path.join(processedDataSrcDir, file), path.join(processedDataDestDir, file));
    console.log(`Copied data: ${file}`);
  });
}

// Preserve docs/data_sources.md by copying it to public/
const dataSourcesSrc = path.join(rootDir, 'docs', 'data_sources.md');
const dataSourcesDest = path.join(__dirname, 'public', 'data_sources.md');
if (fs.existsSync(dataSourcesSrc)) {
  fs.copyFileSync(dataSourcesSrc, dataSourcesDest);
  console.log('Copied data_sources.md to public/');
}

console.log('Asset synchronization complete!');
