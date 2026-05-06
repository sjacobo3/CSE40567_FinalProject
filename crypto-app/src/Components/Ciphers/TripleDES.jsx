import { useState, useEffect } from "react"
import { Typography, Paper, TextField, Box, Button, Select, MenuItem, FormControl } from "@mui/material"

const TripleDES = ({ cipher }) =>  
{
    // define variables
    const [inputType, setInputType] = useState("text")
    const [k1, setK1] = useState("")
    const [k2, setK2] = useState("")
    const [k3, setK3] = useState("")
    const [pt, setPt] = useState("")
    const [ct, setCt] = useState("")
    const [fp, setFp] = useState("")
    const [fd, setFd] = useState(null)
    const [fileExt, setFileExt] = useState("")
    const [pyodide, setPyodide] = useState(null)

    // get my python code
    useEffect(() => {
        const load = async () => {
            const pyodide = await window.loadPyodide()
            const response = await fetch("/Python/TripleDES.py")
            const py_code = await response.text()
            await pyodide.runPythonAsync(py_code)
            setPyodide(pyodide)
        }
        load()
    }, [])

    // define functions
    const tripdes_encrypt = () => {
        if (inputType === "text") {
            // run encryption and retrieve ciphertext
            const ciphertext = pyodide.runPython(`tripdes_encrypt("${pt}", "${k1}", "${k2}", "${k3}")`)
            setCt(ciphertext)
        } else {
            // save file as bytes
            pyodide.globals.set("_filebytes", pyodide.toPy(fd))
            // run encryption and retrieve ciphertext
            const ciphertext = pyodide.runPython(`tripdes_encrypt(bytes(_filebytes), "${k1}", "${k2}", "${k3}")`)
            // download encrypted file
            const blob = new Blob([new TextEncoder().encode(ciphertext)])
            const temp_url = URL.createObjectURL(blob)
            Object.assign(document.createElement("a"), { href: temp_url, download: `encrypted_file${fileExt}` }).click()
            URL.revokeObjectURL(temp_url)
        }
    }
    const tripdes_decrypt = () => {
        if (inputType === "text") {
            // run decryption and retrieve plaintext
            const plaintext = pyodide.runPython(`tripdes_decrypt("${ct}", "${k1}", "${k2}", "${k3}", False)`)
            setPt(plaintext)
        } else {
            // save file as bytes
            pyodide.globals.set("_filebytes", pyodide.toPy(fd))
            // run decryption and retrieve plaintext binary
            const plaintext = pyodide.runPython(`tripdes_decrypt(bytes(_filebytes), "${k1}", "${k2}", "${k3}", True)`)
            // convert to JS array
            const plaintext_js = plaintext.toJs()
            // download decrypted file
            const blob = new Blob([new Uint8Array(plaintext_js)])
            const temp_url = URL.createObjectURL(blob)
            Object.assign(document.createElement("a"), { href: temp_url, download: `decrypted_file${fileExt}` }).click()
            URL.revokeObjectURL(temp_url)
        }
    }
    const file_upload = (e) => {
        // upload file
        const file = e.target.files[0]
        if (!file) return
        setFp(file.name)
        // retrieve file extension to preserve it
        const ext = file.name.substring(file.name.lastIndexOf('.'))
        setFileExt(ext)
        // read the file
        const reader = new FileReader()
        reader.onload = (e1) => setFd(new Uint8Array(e1.target.result))
        reader.readAsArrayBuffer(file)
    }
    const key_upload = (ev, setKn) => {
        // load key
        const file = ev.target.files[0]
        if (!file) return
        // read key
        const reader = new FileReader()
        reader.onload = (e) => setKn(e.target.result.trim())
        reader.readAsText(file)
    }

    return (
        <Paper sx={{ backgroundColor: "white", padding: 2, maxWidth: 800, margin: '0 auto', mt: 4 }}>
            <Typography variant="h2" sx={{ color: "primary.main", textAlign: "center" }}>
                {cipher}
            </Typography>
            <Typography variant="h3" sx={{ color: "tertiary.main", mt: 1 }}>
                Input Type
            </Typography>
            <FormControl variant="standard" fullWidth sx={{ mt: 1 }}>
                <Select value={inputType} onChange={(e) => {setInputType(e.target.value)}}>
                    <MenuItem value="text">Text</MenuItem>
                    <MenuItem value="file">File</MenuItem>
                </Select>
            </FormControl>
            <Typography variant="body1" sx={{ color: "tertiary.main", mt: 2 }}>
                K1:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={k1} onChange={(e) => setK1(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={(e) => key_upload(e, setK1)}/>
                </Button>
            </Box>
            <Typography variant="body1" sx={{ color: "tertiary.main", mt: 1 }}>
                K2:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={k2} onChange={(e) => setK2(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={(e) => key_upload(e, setK2)}/>
                </Button>
            </Box>
            <Typography variant="body1" sx={{ color: "tertiary.main", mt: 1 }}>
                K3:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={k3} onChange={(e) => setK3(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={(e) => key_upload(e, setK3)}/>
                </Button>
            </Box>
            
            {inputType == "text" ? 
                (<><Typography variant="body1" sx={{ color: "tertiary.main", mt: 1 }}>
                    Plaintext:
                </Typography>
                <TextField fullWidth variant="standard" value={pt} onChange={(e) => setPt(e.target.value)}/>
                <Typography variant="body1" sx={{ color: "tertiary.main", mt: 1 }}>
                    Ciphertext:
                </Typography>
                <TextField fullWidth variant="standard" value={ct} onChange={(e) => setCt(e.target.value)}/></>) 
                : 
                ( 
                <><Button component="label" disabled={!pyodide} sx={{ mt: 1, justifyContent: "center", display: "flex", color: "tertiary.main" }}>
                    Upload File
                    <input type="file" hidden onChange={file_upload} disabled={!pyodide}/>
                </Button>
                {fp && (
                    <Typography variant="body2" sx={{ color: "tertiary.main", textAlign: "center", mt: 1 }}>
                        Currently uploaded: {fp}
                    </Typography>
                )}</>)
            }
            <Box sx={{ justifyContent: "center", display: "flex", mt: 6 }}>
                <Button onClick={tripdes_encrypt} disabled={!pyodide} sx={{ backgroundColor: "info.main", "&:hover": {backgroundColor: "info.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Encrypt
                </Button>
                <Button onClick={tripdes_decrypt} disabled={!pyodide} sx={{ backgroundColor: "secondary.main", "&:hover": {backgroundColor: "secondary.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Decrypt
                </Button>
            </Box>
        </Paper>
    )
}

export default TripleDES