const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false           // ✅ 이 줄 추가
    }
  });

  win.loadFile('index.html');

//   // ✅ 여기에 넣으면 됩니다
//   win.webContents.openDevTools(); // 개발자 도구 창 열기
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
