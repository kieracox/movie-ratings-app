editButtons = document.querySelectorAll('.edit-movie-rating');

for (const button of editButtons) {
    button.addEventListener('click', () => {
        const newScore = prompt('What is your new score?')
        const formInputs = {
            updated_score: newScore,
            rating_id: button.id
        };

        fetch('/update_rating', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((response) => {
            if (response.ok) {
                document.querySelector(`span.rating_num_${button.id}`).innerHTML = newScore;
            } else {
                alert('Failed to update rating');
            }
        })
    });
}