document.addEventListener("DOMContentLoaded", function () {
    const driverComparisonForm = document.getElementById("driver-comparison-form");
    const teamComparisonForm = document.getElementById("team-comparison-form");

    if (driverComparisonForm) {
        driverComparisonForm.addEventListener("submit", function (event) {
            event.preventDefault();
            compareDrivers();
        });
    }

    if (teamComparisonForm) {
        teamComparisonForm.addEventListener("submit", function (event) {
            event.preventDefault();
            compareTeams();
        });
    }
});

async function compareDrivers() {
    const driver1Id = document.getElementById("driver1").value;
    const driver2Id = document.getElementById("driver2").value;

    if (!driver1Id || !driver2Id) {
        alert("Please select both drivers to compare.");
        return;
    }

    try {
        const response = await fetch(`/api/compare-drivers?driver1=${driver1Id}&driver2=${driver2Id}`);
        const data = await response.json();

        if (response.ok) {
            displayDriverComparison(data);
        } else {
            alert(data.error || "Error comparing drivers.");
        }
    } catch (error) {
        console.error("Error fetching driver comparison:", error);
        alert("Failed to retrieve driver comparison.");
    }
}

async function compareTeams() {
    const team1Id = document.getElementById("team1").value;
    const team2Id = document.getElementById("team2").value;

    if (!team1Id || !team2Id) {
        alert("Please select both teams to compare.");
        return;
    }

    try {
        const response = await fetch(`/api/compare-teams?team1=${team1Id}&team2=${team2Id}`);
        const data = await response.json();

        if (response.ok) {
            displayTeamComparison(data);
        } else {
            alert(data.error || "Error comparing teams.");
        }
    } catch (error) {
        console.error("Error fetching team comparison:", error);
        alert("Failed to retrieve team comparison.");
    }
}

function displayDriverComparison(data) {
    const resultDiv = document.getElementById("driver-comparison-result");
    resultDiv.innerHTML = `
        <h3>Driver Comparison</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Attribute</th>
                    <th>${data.driver1.name}</th>
                    <th>${data.driver2.name}</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Championships</td><td>${data.driver1.championships}</td><td>${data.driver2.championships}</td></tr>
                <tr><td>Wins</td><td>${data.driver1.wins}</td><td>${data.driver2.wins}</td></tr>
                <tr><td>Podiums</td><td>${data.driver1.podiums}</td><td>${data.driver2.podiums}</td></tr>
                <tr><td>Poles</td><td>${data.driver1.poles}</td><td>${data.driver2.poles}</td></tr>
                <tr><td>Fastest Laps</td><td>${data.driver1.fastest_laps}</td><td>${data.driver2.fastest_laps}</td></tr>
            </tbody>
        </table>
    `;
}

function displayTeamComparison(data) {
    const resultDiv = document.getElementById("team-comparison-result");
    resultDiv.innerHTML = `
        <h3>Team Comparison</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Attribute</th>
                    <th>${data.team1.name}</th>
                    <th>${data.team2.name}</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Championships</td><td>${data.team1.championships}</td><td>${data.team2.championships}</td></tr>
                <tr><td>Wins</td><td>${data.team1.wins}</td><td>${data.team2.wins}</td></tr>
                <tr><td>Podiums</td><td>${data.team1.podiums}</td><td>${data.team2.podiums}</td></tr>
                <tr><td>Pole Positions</td><td>${data.team1.poles}</td><td>${data.team2.poles}</td></tr>
                <tr><td>Fastest Laps</td><td>${data.team1.fastest_laps}</td><td>${data.team2.fastest_laps}</td></tr>
            </tbody>
        </table>
    `;
}
