import { useEffect, useState } from "react"

export default function useMounted() {
    const [isMounted, setIsMounted] = useState(false);
    
    useEffect(()=>{
        setIsMounted(true);
    }, [isMounted]);
    
    return {
        setIsMounted,
        isMounted
    } 
}