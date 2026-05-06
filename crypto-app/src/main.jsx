import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material'

const theme = createTheme({
    palette: {
        primary: {
            light: "#a6b8a5",
            main: "#536953",
            dark: "#304030"
        },
        secondary: {
            light: "#365c8f",
            main: "#183a69",
            dark: "#001f49"
        },
        tertiary: {
            main: "#272727"
        },
        info: {
            light: "#f9f4ed",
            main: "#deae40",
            dark: "#c8982a"
        }
    },
    typography: {
        h1: {
            fontSize: "2.125rem",
            fontWeight: "bold",
            '@media (max-width:600px)': {
                fontSize: "1.75rem",
            }
        },
        h2: {
            fontSize: "1.75rem",
            fontWeight: "bold",
            '@media (max-width:600px)': {
                fontSize: "1.5rem",
            }
        },
        h3: {
            fontSize: "1rem",
            fontWeight: "bold",
            '@media (max-width:600px)': {
                fontSize: "1.25rem",
            }
        },
        body1: {
            fontSize: "1rem",
            fontWeight: "400"
        },
        fontFamily: "'EB Garamond', serif"
        
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    backgroundColor: "#f9f4ed"
                }
            }
        }
    }
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
    <CssBaseline />
        <App /> 
    </ThemeProvider>
  </StrictMode>,
)