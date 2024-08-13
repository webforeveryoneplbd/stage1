document.getElementById('user-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const matricule = document.getElementById('matricule').value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/user/${matricule}`);

        if (response.ok) {
            const userInfo = await response.json();
            document.getElementById('user-info').innerText = JSON.stringify(userInfo, null, 2);
        } else {
            alert('User not found.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching user information.');
    }
});
