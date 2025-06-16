import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import VerifyEmail from "./pages/auth/VerifyEmail";
// import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import EditorPage from "./pages/EditorPage";
import Groups from "./pages/Groups";
import GroupDetail from "./pages/GroupDetail";
import Tasks from "./pages/Tasks";
import TaskDetail from "./pages/TaskDetail";
import Tags from "./pages/Tags";
import Collaborators from "./pages/Collaborators";
import UserProfile from "./pages/UserProfile";
import Notifications from "./pages/Notifications";
import ProjectEdit from "./pages/ProjectEdit";
import ProjectTags from "./pages/ProjectTags";
import FileVersionsPage from "./pages/FileVersionsPage";

export default function App() {
  const { user } = useAuth();

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/projects/:id" element={<ProjectDetail />} />
        <Route path="/editor/:projectId/:fileId" element={<EditorPage />} />
        <Route path="/groups" element={<Groups />} />
        <Route path="/groups/:id" element={<GroupDetail />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/tasks/:id" element={<TaskDetail />} />
        <Route path="/tags" element={<Tags />} />
        <Route path="/collaborators" element={<Collaborators />} />
        <Route path="/users/:id" element={<UserProfile />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/projects/:id/edit" element={<ProjectEdit />} />
        <Route path="/projects/:id/tags" element={<ProjectTags />} />
        <Route path="/files/:fileId/versions" element={<FileVersionsPage />} />
      </Routes>
    </>
  );
}
