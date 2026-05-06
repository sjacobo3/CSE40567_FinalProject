import { Typography, Paper, TextField, Box, Button } from "@mui/material"
import Vigenere from "./Vigenere"
import TripleDES from "./TripleDES"
import RSA from "./RSA"
import AES from "./AES"

const Ciphers = ({cipher}) =>  
{
    if (cipher === "Vigenere") return <Vigenere cipher={cipher}/>
    if (cipher === "3DES") return <TripleDES cipher={cipher}/>
    if (cipher === "RSA") return <RSA cipher={cipher}/>
    if (cipher === "AES") return <AES cipher={cipher}/>
    return null
}

export default Ciphers