import express from "express"
import mongoose from "mongoose"
import { insertBlock, retrieveChain } from "./controllers/insertBlock.js"
const app = express()
app.use(express.json())
const connn =     "mongodb+srv://FinalYearProject:FinalYearProject@cluster0.1ldpglc.mongodb.net/test"
    const conn = await mongoose.connect(connn, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log(`MongoDB connected: ${conn.connection.host}`);
app.post("/blockchain",insertBlock)
app.get("/blocks",retrieveChain)

let port = 5000
app.listen(port,()=>{
    console.log(`example listening on  ${port}`)
})