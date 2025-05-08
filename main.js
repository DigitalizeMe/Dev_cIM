const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
            sandbox: false
        }
    });

    const indexPath = path.join(__dirname, 'dist', 'index.html');
    console.log('Loading index.html from:', indexPath);
    if (!fs.existsSync(indexPath)) {
        console.error('index.html not found at:', indexPath);
    }
    win.loadFile(indexPath).catch(err => {
        console.error('Error loading index.html:', err);
    });
    win.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});