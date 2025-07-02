const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let pythonBackend;

const SERVER_URL = 'http://localhost:5000';

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false
    }
  });

  mainWindow.loadFile('index.html');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startPythonServer() {
  const backendPath = path.join(__dirname, 'backend', 'backend.py');
  pythonBackend = spawn('python', [backendPath]);

  pythonBackend.stdout.on('data', (data) => {
    console.log(`[PYTHON]: ${data}`);
  });

  pythonBackend.stderr.on('data', (data) => {
    console.error(`[PYTHON ERROR]: ${data}`);
  });

  pythonBackend.on('close', (code) => {
    console.log(`Python server exited with code ${code}`);
  });
}

function stopPythonServer() {
  if (pythonBackend) {
    pythonBackend.kill();
  }
}

// 서버 상태 확인 함수
function checkServerStatus() {
  return new Promise((resolve) => {
    http.get(`${SERVER_URL}/api/graph_data`, (res) => {
      if (res.statusCode === 200) {
        resolve(true);
      } else {
        resolve(false);
      }
    }).on('error', () => resolve(false));
  });
}

// 서버에서 API 엔드포인트 목록 조회 (직접 하드코딩하거나, API로 받아올 수 있음)
const apiList = [
  { path: '/api/graph_data', description: '2D 그래프 데이터' },
  { path: '/api/3d_data', description: '3D 그래프 데이터' },
  { path: '/api/sine_wave', description: '사인파 데이터' }
];

// 렌더러에서 서버 상태 요청 받으면 응답
ipcMain.handle('get-server-status', async () => {
  const isUp = await checkServerStatus();
  return { isUp, apiList };
});

// 일정 간격으로 서버 상태 확인 후 렌더러에 이벤트 전송
function startStatusPolling() {
  setInterval(async () => {
    if (mainWindow) {
      const isUp = await checkServerStatus();
      mainWindow.webContents.send('server-status-update', { isUp, apiList });
    }
  }, 5000);  // 5초마다 체크
}

app.whenReady().then(() => {
  createWindow();
  startPythonServer();
  startStatusPolling();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  stopPythonServer();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
