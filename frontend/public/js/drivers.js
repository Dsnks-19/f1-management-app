document.addEventListener("DOMContentLoaded", function () {
    fetchDrivers();
});

async function fetchDrivers() {
    try {
        const response = await fetch("/api/drivers");
        const drivers = await response.json();
        displayDrivers(drivers);
    } catch (error) {
        console.error("Error fetching drivers:", error);
    }
}

function displayDrivers(drivers) {
    const driversTable = document.getElementById("drivers-table");
    driversTable.innerHTML = "";

    drivers.forEach(driver => {
        const row = `<tr>
                        <td>${driver.name}</td>
                        <td>${driver.team}</td>
                        <td>${driver.wins}</td>
                        <td><a href="driver-details.html?id=${driver.id}">View</a></td>
                        <td><a href="edit-driver.html?id=${driver.id}">Edit</a></td>
                        <td><button onclick="deleteDriver('${driver.id}')">Delete</button></td>
                    </tr>`;
        driversTable.innerHTML += row;
    });
}

async function deleteDriver(id) {
    if (!confirm("Are you sure you want to delete this driver?")) return;
    try {
        await fetch(`/api/drivers/${id}`, { method: "DELETE" });
        fetchDrivers();
    } catch (error) {
        console.error("Error deleting driver:", error);
    }
}
