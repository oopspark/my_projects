// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    transparent: false,     // 🔍 배경 투명
    frame: true,          // ❌ 타이틀바 + 기본 버튼 제거
    // resizable: false,      // (선택) 크기 고정
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    }
  });

  win.setMenuBarVisibility(false); // ❌ 메뉴바 제거
  win.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
