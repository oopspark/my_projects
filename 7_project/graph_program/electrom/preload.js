// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  fetchGraphData: (args) => ipcRenderer.invoke('fetch-graph-data', args)
});
