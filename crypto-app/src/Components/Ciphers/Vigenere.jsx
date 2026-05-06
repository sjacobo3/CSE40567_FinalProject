import { useState, useEffect } from "react"
import { Typography, Paper, TextField, Box, Button } from "@mui/material"

const Vigenere = ({ cipher }) =>  
{
    // define variables
    const [k, setK] = useState("")
    const [pt, setPt] = useState("")
    const [ct, setCt] = useState("")
    const [pyodide, setPyodide] = useState(null)

    // get my python code
    useEffect(() => {
        const load = async () => {
            const pyodide = await window.loadPyodide()
            const response = await fetch("/Python/Vigenere.py")
            const py_code = await response.text()
            await pyodide.runPythonAsync(py_code)
            setPyodide(pyodide)
        }
        load()
    }, [])

    // define functions
    const vigenere_encrypt = () => {
        const ciphertext = pyodide.runPython(`vig_encrypt("${pt}", "${k}")`)
        setCt(ciphertext)
    }
    const vigenere_decrypt = () => {
        const plaintext = pyodide.runPython(`vig_decrypt("${ct}", "${k}")`)
        setPt(plaintext)
    }
    const key_import = (e) => {
        const file = e.target.files[0]
        if (!file) return
        const filereader = new FileReader()
        filereader.onload = (e1) => setK(e1.target.result.trim())
        filereader.readAsText(file)
    }

    return (
        <Paper sx={{ backgroundColor: "white", padding: 2, maxWidth: 800, margin: '0 auto', mt: 4 }}>
            <Typography variant="h2" sx={{ color: "primary.main", textAlign: "center" }}>
                {cipher}
            </Typography>
            <Typography variant="body1" sx={{ color: "tertiary.dark", mt: 1 }}>
                Key:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={k} onChange={(e) => setK(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={key_import}/>
                </Button>
            </Box>
            <Typography variant="body1" sx={{ color: "tertiary.dark", mt: 1 }}>
                Plaintext:
            </Typography>
            <TextField fullWidth variant="standard" value={pt} onChange={(e) => setPt(e.target.value)}/>
            <Typography variant="body1" sx={{ color: "tertiary.dark", mt: 1 }}>
                Ciphertext:
            </Typography>
            <TextField fullWidth variant="standard" value={ct} onChange={(e) => setCt(e.target.value)}/>
            <Box sx={{ justifyContent: "center", display: "flex", mt: 6 }}>
                <Button onClick={vigenere_encrypt} disabled={!pyodide} sx={{ backgroundColor: "info.main", "&:hover": {backgroundColor: "info.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Encrypt
                </Button>
                <Button onClick={vigenere_decrypt} disabled={!pyodide} sx={{ backgroundColor: "secondary.main", "&:hover": {backgroundColor: "secondary.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Decrypt
                </Button>
            </Box>
        </Paper>
    )
}

export default Vigenere