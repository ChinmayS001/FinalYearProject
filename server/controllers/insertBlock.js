import Block from "../models/Block.js"
export const insertBlock = async (req,res) =>{

    let index

    if(req.body.chain.length==1){
        index = 0;
        req.body.chain[0].transactions = req.body.chain[0].transactions[0]
        const opp = await Block.create(req.body.chain[0]);
        //console.log("Life Sucks")
        res.send(index);
        return;
    }


    const op = await Block.find().sort({ index: -1 }).limit(1).exec()
    console.log("op: ",op)


    if(!op){
        index = 0;
        const opp = await Block.insertMany(req.body.chain);
        opp.save()
        //console.log("Life Sucks")
        res.send(index);
        return;
    }


   index = op.index+1
   req.body.chain.splice(0,index);
   console.log("Entire Chain",req.body.chain);

   console.log("Index:  ",index,"request chain Index:  ",req.body.chain[req.body.chain.length-1].index)
    for(const i of req.body.chain){
    i.transactions = i.transactions[0]
    await Block.create(i);
    console.log("Inserted Block",i)
    }


    // i.transactions = i.transactions[0];


    //await Block.create(i);
}

export const retrieveChain = async (req,res) =>{
    const op = await Block.find()
    res.json(op);
}