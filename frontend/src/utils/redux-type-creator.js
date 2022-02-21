const createType = (...type)=>{
    return type.reduce((acc, curr)=>{
        acc[curr]= curr
        return acc
    }, {})
}

export default createType