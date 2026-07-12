// script.js

// Welcome message
window.onload = function () {
    console.log("Automated Student Verification System Loaded Successfully");
};

// Delete confirmation
function confirmDelete(regNo) {
    return confirm("Are you sure you want to delete student " + regNo + "?");
}

// Verification confirmation
function confirmVerify(regNo) {
    return confirm("Verify student " + regNo + "?");
}

// Live search
function searchTable() {

    let input = document.getElementById("searchInput");
    let filter = input.value.toUpperCase();

    let table = document.getElementById("studentTable");

    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td");

        let found = false;

        for (let j = 0; j < td.length; j++) {

            if (td[j]) {

                let txt = td[j].textContent || td[j].innerText;

                if (txt.toUpperCase().indexOf(filter) > -1) {

                    found = true;

                }

            }

        }

        tr[i].style.display = found ? "" : "none";

    }

}

// Counter Animation

function animateValue(id, start, end, duration) {

    let obj = document.getElementById(id);

    if (!obj) return;

    let range = end - start;

    let current = start;

    let increment = end > start ? 1 : -1;

    let stepTime = Math.abs(Math.floor(duration / range));

    let timer = setInterval(function () {

        current += increment;

        obj.innerHTML = current;

        if (current == end) {

            clearInterval(timer);

        }

    }, stepTime);

}

window.onload = function () {

    animateValue("totalStudents",0,100,1500);

    animateValue("verifiedStudents",0,75,1500);

    animateValue("pendingStudents",0,25,1500);

};