import Block from "../models/Block.js"
export const insertBlock = async (req,res) =>{

    let index
  //  console.log(req.body.chain);
   


    const op = await Block.find().sort({ index: -1 }).limit(1).exec() //Find the block with the highest index
  //  console.log("op: ",op)   // print the latest block


    if(!op.length){//If there are no blocks
        if(req.body.chain.length==1){ //First block wrong, not necessarily the first block for the database
            index = 0;                  //case 3
            req.body.chain[0].transactions = req.body.chain[0].transactions[0]
            const opp = await Block.create(req.body.chain[0]);
            //console.log("Life Sucks")
         //   console.log("Correct");
            res.send({index});
            return;
        }
        index = 0;                                       //case 4
        //opp.save()
        //console.log("Life Sucks")
        for(const i of req.body.chain){
            i.transactions = i.transactions[0] //remove this to make it not a array
            await Block.create(i);
        //    console.log("Inserted Block",i)
        }
        
        res.send({index});
        return;
    }


   index = op[0].index+1
   req.body.chain.splice(0,index);
 //  console.log("Entire Chain",req.body.chain);

  // console.log("Index:  ",index,"Last block:  ",req.body.chain[req.body.chain.length-1].index)
    for(const i of req.body.chain){
    i.transactions = i.transactions[0] //remove this to make it not a array
    await Block.create(i);
   // console.log("Inserted Block",i)
    }
   res.send({index});

    // i.transactions = i.transactions[0];


    //await Block.create(i);
}

export const retrieveChain = async (req,res) =>{
    const op = await Block.find()
    res.json(op);
}