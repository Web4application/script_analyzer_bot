const { app, ipcMain, BrowserWindow, Menu, Tray } = require("electron")
const fs = require("fs")
const path = require("path")

let mainWindow
let tray = null

function createWindow () {
  app.setName("Web4") // official app name

  // Path to your rainbow logo
  const iconPath = path.join(__dirname, "web4_rainbow.png")

  if (process.platform === "linux" && process.env.APPDIR != null) {
    tray = new Tray(iconPath) // rainbow logo for tray
    const contextMenu = Menu.buildFromTemplate([
      { label: "Item1", type: "radio" },
      { label: "Item2", type: "radio" },
      { label: "Item3", type: "radio", checked: true },
      { label: "Item4", type: "radio" }
    ])
    tray.setToolTip("Web4 Application")
    tray.setContextMenu(contextMenu)
  }

  // Create the browser window with rainbow logo as app icon
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    title: "Web4",
    icon: iconPath // window icon (title bar + taskbar/dock)
  })

  mainWindow.loadURL("file://" + __dirname + "/index.html")
  mainWindow.webContents.openDevTools()

  mainWindow.webContents.executeJavaScript(
    `console.log("appData: ${app.getPath("appData").replace(/\\/g, "\\\\")}")`
  )
  mainWindow.webContents.executeJavaScript(
    `console.log("userData: ${app.getPath("userData").replace(/\\/g, "\\\\")}")`
  )

  mainWindow.on("closed", function () {
    mainWindow = null
  })
}

app.on("ready", createWindow)

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") {
    app.quit()
  }
})

app.on("activate", function () {
  if (mainWindow === null) {
    createWindow()
  }
})

ipcMain.on("saveAppData", () => {
  try {
    fs.writeFileSync(
      path.join(app.getPath("appData"), "Web4", "testFile"),
      "test"
    )
  } catch (e) {
    mainWindow.webContents.executeJavaScript(`console.log(\`userData: ${e}\`)`)
  }
})
