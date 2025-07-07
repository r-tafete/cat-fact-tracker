import { useState, useEffect } from "react";
import "../styles/RandomCatFact.styles.css";


export default function RandomCatFact() {
    const [randomCatFact, setRandomCatFact] = useState("");

    // fetch random cat fact from database
    const getRandomCatFact = async () => {
        try {
            const response = await fetch("http://localhost:8000/catfacts/random");
            const data = await response.json()
            setRandomCatFact(data.fact)
        } catch (error) {
            console.error("Error fetching random cat fact! ", error)
        }
    }

    // call fetch on initial component load
    useEffect(() => {
        getRandomCatFact();
    }, []);


    return (
        <section>
            <h2>Random cat fact!</h2>
            <div className="random-cat-fact">
                <p>{randomCatFact}</p>
                <button onClick={getRandomCatFact}>Another one! 🐈‍⬛</button>
            </div>
        </section>
    );
}
