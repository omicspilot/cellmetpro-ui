import { ThemeToggle } from "@/components/theme-toggle";
import { Outlet } from "react-router-dom";

export default function RootLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background text-foreground">
      {/* Sidebar — wired in 2.3 with React Router */}
      <aside className="w-64 shrink-0 border-r border-border" />

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-14 shrink-0 items-center justify-end border-b border-border px-4">
          <ThemeToggle />
        </header>

        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
