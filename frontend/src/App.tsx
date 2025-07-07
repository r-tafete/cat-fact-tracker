import { useEffect, useState } from "react";
import AllCatFacts from "./components/AllCatFacts"
import RandomCatFact from "./components/RandomCatFact";
import type { CatFact } from "./types";
import CatFactForm from "./components/CatFactForm";

export default function App() {
  const [catFacts, setCatFacts] = useState<CatFact[]>([]);

  // fetch all cat facts from database (used on initial load and when new fact is added)
  const getCatFacts = async () => {
    try {
      const response = await fetch("http://localhost:8000/catfacts/");
      const data = await response.json()
      setCatFacts(data)
    } catch (error) {
      console.error("Error fetching cat facts! ", error)
    }
  }
  
  // call fetch on initial app load
  useEffect(() => {
    getCatFacts();
  }, []);

  return (
    <>
      <header>
        <h1>Cat Fact Tracker 🐈</h1>
      </header>
      <RandomCatFact />
      <CatFactForm onSuccess={getCatFacts} />
      <AllCatFacts catFacts={catFacts} />
    </>
  )
}