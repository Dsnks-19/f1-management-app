document.addEventListener("DOMContentLoaded", function () {
    const driverQueryForm = document.getElementById("driverQueryForm");
    const teamQueryForm = document.getElementById("teamQueryForm");
    const driverResults = document.getElementById("driverResults");
    const teamResults = document.getElementById("teamResults");

    driverQueryForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const queryType = document.getElementById("driverQueryType").value;
        const queryValue = document.getElementById("driverQueryValue").value;

        const response = await fetch(`/api/drivers/query?type=${queryType}&value=${queryValue}`);
        const data = await response.json();
        displayDrivers(data);
    });

    teamQueryForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const queryType = document.getElementById("teamQueryType").value;
        const queryValue = document.getElementById("teamQueryValue").value;

        const response = await fetch(`/api/teams/query?type=${queryType}&value=${queryValue}`);
        const data = await response.json();
        displayTeams(data);
    });

    function displayDrivers(drivers) {
        driverResults.innerHTML = "";
        drivers.forEach(driver => {
            driverResults.innerHTML += `
                <tr>
                    <td>${driver.name}</td>
                    <td>${driver.team}</td>
                    <td>${driver.wins}</td>
                    <td><a href="driver-details.html?id=${driver.id}" class="btn btn-info">View</a></td>
                </tr>`;
        });
    }

    function displayTeams(teams) {
        teamResults.innerHTML = "";
        teams.forEach(team => {
            teamResults.innerHTML += `
                <tr>
                    <td>${team.name}</td>
                    <td>${team.championships}</td>
                    <td>${team.founded}</td>
                    <td><a href="team-details.html?id=${team.id}" class="btn btn-info">View</a></td>
                </tr>`;
        });
    }
});
