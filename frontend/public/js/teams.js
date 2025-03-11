// teams.js

document.addEventListener("DOMContentLoaded", function () {
    fetchTeams();
});

async function fetchTeams() {
    try {
        const response = await fetch("/api/teams");
        const teams = await response.json();
        displayTeams(teams);
    } catch (error) {
        console.error("Error fetching teams:", error);
    }
}

function displayTeams(teams) {
    const tableBody = document.getElementById("teams-table-body");
    tableBody.innerHTML = "";
    teams.forEach(team => {
        const row = `<tr>
                        <td>${team.name}</td>
                        <td>${team.principal}</td>
                        <td>${team.wins}</td>
                        <td>
                            <a href="team-details.html?id=${team.id}">View</a>
                            <a href="edit-team.html?id=${team.id}">Edit</a>
                            <button onclick="deleteTeam('${team.id}')">Delete</button>
                        </td>
                    </tr>`;
        tableBody.innerHTML += row;
    });
}

async function deleteTeam(teamId) {
    if (!confirm("Are you sure you want to delete this team?")) return;
    try {
        await fetch(`/api/teams/${teamId}`, { method: "DELETE" });
        fetchTeams();
    } catch (error) {
        console.error("Error deleting team:", error);
    }
}
