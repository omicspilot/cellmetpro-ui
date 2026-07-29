import { createHashRouter } from "react-router-dom"

import ProjectDetailPage from "./pages/project-detail"
import ProjectListPage from "./pages/project-list"
import RootLayout from "./layouts/root-layout"
import SettingsPage from "./pages/settings"

export default createHashRouter([
  {
    path: "/",
    element: <RootLayout />, // ← the shell (sidebar + header)
    children: [
      { index: true, element: <ProjectListPage /> },
      { path: "projects/:projectId", element: <ProjectDetailPage /> },
      { path: "settings", element: <SettingsPage /> },
    ],
  },
])
