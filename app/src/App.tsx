import { useState } from 'react'
import './App.css'
import { ThemeProvider } from './components/theme-provider'
import { Card, CardContent} from './components/ui/card'

function App() {

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Card className="w-full max-w-sm m-2">
        <CardContent>
          Chicken Parmasan Rice
        </CardContent>
      </Card>
      <Card className="w-full max-w-sm m-2">
        <CardContent>
          Jambalia
        </CardContent>
      </Card>
      <Card className="w-full max-w-sm m-2">
        <CardContent>
          Lasagna
        </CardContent>
      </Card>
      <Card className="w-full max-w-sm m-2">
        <CardContent>
          Tacos
        </CardContent>
      </Card>
    </ThemeProvider>
  )
}

export default App
