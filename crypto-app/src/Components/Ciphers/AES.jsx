import { useState, useEffect } from "react"
import { Typography, Paper, TextField, Box, Button, Select, MenuItem, FormControl } from "@mui/material"

const AES = ({ cipher }) =>  
{
    // define variables
    const [inputType, setInputType] = useState("text")
    const [k, setK] = useState("")
    const [pt, setPt] = useState("")
    const [ct, setCt] = useState("")
    const [fp, setFp] = useState("")
    const [fd, setFd] = useState("")
    const [fileExt, setFileExt] = useState("")
    const [pyodide, setPyodide] = useState(null)

    // get my python code
    useEffect(() => {
        const load = async () => {
            const pyodide = await window.loadPyodide()
            const response = await fetch("/Python/AES.py")
            const py_code = await response.text()
            await pyodide.runPythonAsync(py_code)
            setPyodide(pyodide)
        }
        load()
    }, [])

    // define functions
    const aes_encrypt = () => {
        // convert key to an array and save it
        pyodide.globals.set("_keybytes", pyodide.toPy(Array.from(k).map(c => c.charCodeAt(0))))

        if (inputType === "text") {
            // run encryption and retrieve ciphertext
            const ciphertext = pyodide.runPython(`aes_encrypt_text(${JSON.stringify(pt)}, _keybytes)`)
            // convert to JS array
            const ciphertext_js = ciphertext.toJs()
            setCt(Array.from(ciphertext_js).map(b => b.toString(16).padStart(2, '0')).join(''))
        } else {
            // save file as bytes
            pyodide.globals.set("_filebytes", pyodide.toPy(fd))
            // run encryption and retrieve ciphertext
            const ciphertext = pyodide.runPython(`aes_encrypt_file(bytes(_filebytes), _keybytes)`)
            // convert to JS array
            const ciphertext_js = ciphertext.toJs()
            // download encrypted file
            const blob = new Blob([new Uint8Array(ciphertext_js)])
            const temp_url = URL.createObjectURL(blob)
            Object.assign(document.createElement("a"), { href: temp_url, download: `encrypted_file${fileExt}` }).click()
            URL.revokeObjectURL(temp_url)
        }
    }
    const aes_decrypt = () => {
        // convert key to an array and save it
        pyodide.globals.set("_keybytes", pyodide.toPy(Array.from(k).map(c => c.charCodeAt(0))))

        if (inputType === "text") {
            const ciphertext = `[${ct.match(/.{1,2}/g).map(h => parseInt(h, 16))}]`
            // run decryption and retrieve plaintext
            const plaintext = pyodide.runPython(`aes_decrypt_text(${ciphertext}, _keybytes)`)
            setPt(plaintext)
        } else {
            // save file as bytes
            pyodide.globals.set("_filebytes", pyodide.toPy(fd))
            // run decryption and retrieve plaintext
            const plaintext = pyodide.runPython(`aes_decrypt_file(bytes(_filebytes), _keybytes)`)
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
        const file = e.target.files[0]
        if (!file) return
        setFp(file.name)
        const ext = file.name.substring(file.name.lastIndexOf('.'))
        setFileExt(ext)
        const reader = new FileReader()
        reader.onload = (e1) => setFd(new Uint8Array(e1.target.result))
        reader.readAsArrayBuffer(file)
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
            <Typography variant="h3" sx={{ color: "tertiary.main", mt: 1 }}>
                Input Type
            </Typography>
            <FormControl variant="standard" fullWidth sx={{ mt: 1 }}>
                <Select value={inputType} onChange={(e) => setInputType(e.target.value)}>
                    <MenuItem value="text">Text</MenuItem>
                    <MenuItem value="file">File</MenuItem>
                </Select>
            </FormControl>
            <Typography variant="body1" sx={{ color: "tertiary.dark", mt: 1 }}>
                Key (16 characters):
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
                <TextField fullWidth variant="standard" value={k} onChange={(e) => setK(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={key_import}/>
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
                <Button onClick={aes_encrypt} disabled={!pyodide} sx={{ backgroundColor: "info.main", "&:hover": {backgroundColor: "info.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Encrypt
                </Button>
                <Button onClick={aes_decrypt} disabled={!pyodide} sx={{ backgroundColor: "secondary.main", "&:hover": {backgroundColor: "secondary.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Decrypt
                </Button>
            </Box>
        </Paper>
    )
}

export default AES