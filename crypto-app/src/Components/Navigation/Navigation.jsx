import { useState } from "react"
import { Typography, Box, Button, Paper, TextField } from "@mui/material"
import Ciphers from "../Ciphers/Ciphers"

const ciphers = ["Vigenere", "3DES", "RSA", "AES"];

const Navigation = () =>  
{
    // default cipher shown is vigenere
    const [active, setActive] = useState("Vigenere")

    return (
        <Box sx= {{ mt: 4 }}>
            <Paper sx={{ backgroundColor: "primary.main", padding: 2, maxWidth: 600, margin: '0 auto' }}>
                <Typography variant="h1" sx={{ color: "white", textAlign: "center" }}> 
                    Cipher Algorithm Tool
                </Typography>
                <Typography variant="body1" sx={{ color: "white", mt: 1, textAlign: "center" }}>
                    Choose one of the ciphers below to encrypt and decrypt!
                </Typography>
            </Paper>
            <Box sx={{ justifyContent: "center", display: "flex", mt: 6 }}>
                {ciphers.map((cipher) => (
                    <Button key={cipher} onClick={() => setActive(cipher)} sx={{ backgroundColor: active === cipher ? "primary.main" : "primary.light", "&:hover": {backgroundColor: "primary.main"}, color: "white", mr: 2, ml: 2 }}>
                    {cipher}
                    </Button>
                ))}
            </Box>
            <Ciphers cipher={active}/>
        </Box>
    )
}

export default Navigation