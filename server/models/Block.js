import mongoose from "mongoose";
const BlockSchema = mongoose.Schema({
    index: { type: Number, required:true},
    transactions: {type: String},
    timestamp: {type:Date},
    previous_hash : {type:String},
    nonce: {type: Number},
    hash: {type: String}
})
export default mongoose.model("Block",BlockSchema)