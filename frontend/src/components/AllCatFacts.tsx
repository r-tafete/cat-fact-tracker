import type { CatFact } from "../types";

export default function AllCatFacts(props: { catFacts: CatFact[] }) {
    return (
        <section>
            <h2>Cat Facts!</h2>
            <ul>
                {props.catFacts.map((catFact) => (
                    <li>{catFact.fact}</li>
                ))}
            </ul>
        </section>
    );
}

