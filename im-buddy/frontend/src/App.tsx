import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import Homepage from "./Components/homepage"
function App() {
  const queryClient = new QueryClient()
  return (
    <QueryClientProvider client={queryClient}>
      <Homepage />
    </QueryClientProvider>
  )
}

export default App
