import { useState, type FormEvent } from "react";

export default function CatFactForm(props: { onSuccess: () => void }) {
    const [newFact, setNewFact] = useState("");

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        try {
            // add new cat fact to query search params and send POST request to database
            const params = new URLSearchParams({ cat_fact: newFact });
            const response = await fetch(`http://localhost:8000/catfacts?${params.toString()}`, {
                method: "POST",
            });

            // if successful, clear input state and call onSuccess callback (triggers refresh in app)
            if (response.ok) {
                setNewFact("");
                props.onSuccess();
            }
        } catch (error) {
            console.error("Error submitting cat fact:", error);
        }
    };

    return (
        <section>
            <h2>Know another cat fact? Add it to our database!</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={newFact}
                    onChange={(e) => setNewFact(e.target.value)}
                    placeholder="Enter a new cat fact"
                />
                <button type="submit">Add cat fact!</button>
            </form>
        </section>
    );
}
