import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";

export default function App() {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem
      disableTransitionOnChange
    >
      <div className="flex h-screen overflow-hidden bg-background text-foreground">
        {/* Sidebar — wired in 2.3 with React Router */}
        <aside className="w-64 shrink-0 border-r border-border" />

        {/* Main content area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          <header className="flex h-14 shrink-0 items-center justify-end border-b border-border px-4">
            <ThemeToggle />
          </header>

          <main className="flex-1 overflow-auto p-6">
            {/* Router outlet goes here in 2.3 */}
          </main>
        </div>
      </div>
    </ThemeProvider>
  );
}
