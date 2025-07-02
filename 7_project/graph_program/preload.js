const { contextBridge, ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

contextBridge.exposeInMainWorld('electronAPI', {
  readDataFile: (filename) => {
    const filePath = path.join(__dirname, 'data', filename);
    try {
      const data = fs.readFileSync(filePath, 'utf-8');
      return data;
    } catch(e) {
      return null;
    }
  }
});
