import { useParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import api from "../api/axios";
import SaveVersionButton from "../components/SaveVersionButton";

export default function EditorPage() {
  const { projectId, fileId } = useParams();
  const [content, setContent] = useState("// Загрузка...");
  const [language, setLanguage] = useState("plaintext");
  const socketRef = useRef(null);
  const editorRef = useRef(null);
  const lastSentContentRef = useRef("");
  const saveTimeoutRef = useRef(null);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const [filename, setFilename] = useState("file.txt");

  useEffect(() => {
    // 1. Получаем язык и содержимое
    api.get(`/files/${fileId}`).then((res) => {
      setLanguage(getLanguageFromFilename(res.data.filename));
      setFilename(res.data.filename);
      api.get(`/files/${fileId}/read`).then((res2) => {
        setContent(res2.data);
        lastSentContentRef.current = res2.data;
      });
    });

    // 2. Подключаем WebSocket
    const ws = new WebSocket(`ws://localhost:8000/editor/ws/${projectId}/${fileId}`);
    socketRef.current = ws;

    ws.onmessage = (event) => {
      if (!editorRef.current) return;
      const editor = editorRef.current;
      const incoming = event.data;
      const current = editor.getValue();

      // 💡 не обновляем, если уже текущее значение такое
      if (current !== incoming) {
        editor.setValue(incoming);
        lastSentContentRef.current = incoming;
      }
    };

    return () => ws.close();
  }, [fileId, projectId]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const content = editorRef.current?.getValue();
        if (content) {
          saveFile(content);
        }
      }
    };
  
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleEditorChange = (value) => {
    if (!socketRef.current || !value) return;

    // 💡 не отправляем, если значение не изменилось
    if (value !== lastSentContentRef.current) {
      lastSentContentRef.current = value;
      socketRef.current.send(value);
    }

    if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
    saveTimeoutRef.current = setTimeout(() => {
      saveFile(value);
    }, 30000);
  };

  const saveFile = async (text) => {
    try {
      setIsSaving(true);
      await api.put(`/files/${fileId}/save`, text, {
        headers: {
          "Content-Type": "text/plain",
        },
      });
      setLastSaved(new Date());
    } catch (err) {
      console.error("Ошибка при сохранении файла", err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="h-screen">
      <div className="absolute top-2 right-4 text-sm text-gray-300">
        {isSaving ? (
          <span>💾 Сохраняю...</span>
        ) : lastSaved ? (
          <span className="text-green-400">✅ Сохранено {formatTime(lastSaved)}</span>
        ) : (
          <span>⌛ Ожидание изменений</span>
        )}
      </div>
      <div className="p-4 bg-gray-900">
        <div className="flex justify-between items-center mb-2">
          <SaveVersionButton fileId={fileId} getContent={() => editorRef.current?.getValue()} />
        </div>
      </div>
      <Editor
        height="100%"
        language={language}
        value={content}
        onChange={handleEditorChange}
        onMount={(editor) => (editorRef.current = editor)}
        theme="vs-dark"
      />
    </div>
  );
}

// 🔍 Функция для определения языка по расширению
function getLanguageFromFilename(filename) {
  const ext = filename.split('.').pop();

  const extensionMap = {
    js: "javascript",
    jsx: "javascript",
    ts: "typescript",
    tsx: "typescript",
    py: "python",
    html: "html",
    css: "css",
    json: "json",
    md: "markdown",
    java: "java",
    cpp: "cpp",
    c: "c",
    cs: "csharp",
    php: "php",
    xml: "xml",
    sh: "shell",
    sql: "sql",
    yaml: "yaml",
    yml: "yaml",
    txt: "plaintext",
  };

  console.log(ext);
  console.log(extensionMap[ext]);

  return extensionMap[ext] || "plaintext";
}


const formatTime = (date) =>
  date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

