import { useState, useEffect } from "react"
import { Typography, Paper, TextField, Box, Button, Select, MenuItem, FormControl, InputLabel } from "@mui/material"

const RSA = ({ cipher }) =>  
{
    // define variables
    const [inputType, setInputType] = useState("text")
    const [e, setE] = useState("")
    const [n, setN] = useState("")
    const [d, setD] = useState("")
    const [pt, setPt] = useState("")
    const [ct, setCt] = useState("")
    const [fp, setFp] = useState("")
    const [fdBin, setFdBin] = useState(null)
    const [fdTxt, setFdTxt] = useState(null)
    const [fileExt, setFileExt] = useState("")
    const [pyodide, setPyodide] = useState(null)

    // get my python code
    useEffect(() => {
        const load = async () => {
            const pyodide = await window.loadPyodide()
            const response = await fetch("/Python/RSA.py")
            const py_code = await response.text()
            await pyodide.runPythonAsync(py_code)
            setPyodide(pyodide)
        }
        load()
    }, [])

    // define functions
    const rsa_encrypt = () => {
        if (inputType === "text") {
            // run encryption and retrieve ciphertext
            const ciphertext = pyodide.runPython(`rsa_encrypt_text(${JSON.stringify(pt)}, int("${e}"), int("${n}"))`)
            setCt(ciphertext)
        } else {
            // save file as bytes
            pyodide.globals.set("_filebytes", pyodide.toPy(fdBin))
            // run encryption and retrieve ciphertext
            const ciphertext = pyodide.runPython(`rsa_encrypt_file(bytes(_filebytes), int("${e}"), int("${n}"))`)
            // download encrypted file
            const blob = new Blob([ciphertext], { type: "text/plain" })
            const temp_url = URL.createObjectURL(blob)
            Object.assign(document.createElement("a"), { href: temp_url, download: `encrypted_file${fileExt}` }).click()
            URL.revokeObjectURL(temp_url)
        }
    }
    const rsa_decrypt = () => {
        if (inputType === "text") {
            // run encryption and retrieve plaintext
            const plaintext = pyodide.runPython(`rsa_decrypt_text(${JSON.stringify(ct)}, int("${d}"), int("${n}"))`)
            setPt(plaintext)
        } else {
            // save file as text
            pyodide.globals.set("_filetext", fdTxt)
            // run decryption and retrieve plaintext
            const plaintext = pyodide.runPython(`rsa_decrypt_file(_filetext, int("${d}"), int("${n}"))`)
            // convert to JS array
            const plaintext_js = plaintext.toJs()
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
        // encryption: read as binary
        const readerBin = new FileReader()
        readerBin.onload = (e1) => setFdBin(new Uint8Array(e1.target.result))
        readerBin.readAsArrayBuffer(file)
        // decryption: read as text
        const readerTxt = new FileReader()
        readerTxt.onload = (e1) => setFdTxt(e1.target.result)
        readerTxt.readAsText(file)
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
                <Select value={inputType} onChange={(e) => setInputType(e.target.value)}>
                    <MenuItem value="text">Text</MenuItem>
                    <MenuItem value="file">File</MenuItem>
                </Select>
            </FormControl>
            <Typography variant="body1" sx={{ color: "tertiary.main", mt: 2 }}>
                e:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={e} onChange={(e) => setE(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={(e) => key_upload(e, setE)}/>
                </Button>
            </Box>
            <Typography variant="body1" sx={{ color: "tertiary.main", mt: 1 }}>
                n (minimum 16 bits):
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={n} onChange={(e) => setN(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={(e) => key_upload(e, setN)}/>
                </Button>
            </Box>
            <Typography variant="body1" sx={{ color: "tertiary.main", mt: 1 }}>
                d:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "flex-end" }}>
            <TextField fullWidth variant="standard" value={d} onChange={(e) => setD(e.target.value)}/>
                <Button component="label" sx={{ whiteSpace: "nowrap", color: "tertiary.main" }}>
                    Import Key
                    <input type="file" hidden accept="*" onChange={(e) => key_upload(e, setD)}/>
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
                <Button onClick={rsa_encrypt} disabled={!pyodide} sx={{ backgroundColor: "info.main", "&:hover": {backgroundColor: "info.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Encrypt
                </Button>
                <Button onClick={rsa_decrypt} disabled={!pyodide} sx={{ backgroundColor: "secondary.main", "&:hover": {backgroundColor: "secondary.dark"}, color: "white", mr: 2, ml: 2 }}>
                    Decrypt
                </Button>
            </Box>
        </Paper>
    )
}

export default RSA