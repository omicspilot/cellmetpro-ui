import { Outlet } from "react-router-dom"

import { cn } from "@/lib/utils"
import { useConnectionStore } from "@/store/connection"
import { ThemeToggle } from "@/components/theme-toggle"

export default function RootLayout() {
  const status = useConnectionStore((s) => s.status)

  const dotColor = {
    idle: "bg-muted-foreground",
    checking: "bg-yellow-400",
    connected: "bg-green-500",
    error: "bg-destructive",
  }[status]

  return (
    <div className="flex h-screen overflow-hidden bg-background text-foreground">
      {/* Sidebar — wired in 2.3 with React Router */}
      <aside className="w-64 shrink-0 border-r border-border" />

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <header
          className={cn(
            "flex h-14 shrink-0 items-center justify-end border-b border-border",
            "gap-3 px-4"
          )}
        >
          <ThemeToggle />
          <div className={cn("size-2 rounded-full", dotColor)} />
        </header>

        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
