import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

function App() {
  const queryClient = new QueryClient()
  return (
    <QueryClientProvider client={queryClient}>
    <div className="flex justify-center items-center h-screen w-screen bg-secondary">
      <h1 className="text-3xl font-bold text-secondary-foreground">Hello world!</h1>
    </div>
    </QueryClientProvider>
  )
}

export default App
