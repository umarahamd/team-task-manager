const API = "http://127.0.0.1:5000";

let allTasks = []; // store tasks for filtering

// 🔐 LOGIN
async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch(API + "/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (data.token) {
            localStorage.setItem("token", data.token);
            alert("Login successful");

            loadDashboard();
            loadTasks();
        } else {
            alert(data.msg || "Login failed");
        }

    } catch (err) {
        console.error(err);
        alert("Login error");
    }
}


// 📁 CREATE PROJECT
async function createProject() {
    const name = document.getElementById("projectName").value;
    const token = localStorage.getItem("token");

    if (!token) return alert("Please login first");

    try {
        await fetch(API + "/projects", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ name })
        });

        alert("Project Created");

    } catch (err) {
        console.error(err);
        alert("Error creating project");
    }
}


// 📌 CREATE TASK
async function createTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("desc").value;
    const due_date = document.getElementById("date").value;
    const token = localStorage.getItem("token");

    if (!token) return alert("Please login first");

    try {
        await fetch(API + "/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                title,
                description,
                due_date,
                project_id: 1
            })
        });

        alert("Task Created");

        loadTasks();
        loadDashboard();

    } catch (err) {
        console.error(err);
        alert("Error creating task");
    }
}


// 📊 DASHBOARD
async function loadDashboard() {
    const token = localStorage.getItem("token");

    if (!token) return;

    try {
        const res = await fetch(API + "/dashboard", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        document.getElementById("stats").innerHTML = `
            <div class="stat total">Total<br>${data.total}</div>
            <div class="stat completed">Completed<br>${data.completed}</div>
            <div class="stat pending">Pending<br>${data.pending}</div>
            <div class="stat overdue">Overdue<br>${data.overdue}</div>
        `;

    } catch (err) {
        console.error(err);
    }
}


// 📋 LOAD TASKS
async function loadTasks() {
    const token = localStorage.getItem("token");

    if (!token) return;

    try {
        const res = await fetch(API + "/tasks", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        allTasks = await res.json();
        renderTasks(allTasks);

    } catch (err) {
        console.error(err);
    }
}


// 🎨 RENDER TASKS
function renderTasks(tasks) {
    const html = tasks.map(t => `
        <div class="task">
            <b>${t.title}</b> 
            <span style="float:right;">${t.status}</span><br>
            ${t.description}<br>
            <small>Due: ${t.due_date}</small><br>

            <button onclick="markComplete(${t.id})">✔</button>
            <button onclick="deleteTask(${t.id})">🗑</button>
        </div>
    `).join("");

    document.getElementById("tasks").innerHTML = html;
}


// ❌ DELETE TASK
async function deleteTask(id) {
    const token = localStorage.getItem("token");

    await fetch(API + "/tasks/" + id, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    loadTasks();
    loadDashboard();
}


// ✔ MARK COMPLETE
async function markComplete(id) {
    const token = localStorage.getItem("token");

    await fetch(API + "/tasks/" + id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ status: "Completed" })
    });

    loadTasks();
    loadDashboard();
}


// 🔍 FILTER TASKS
function filterTasks(status) {
    if (status === "All") {
        renderTasks(allTasks);
    } else {
        const filtered = allTasks.filter(t => t.status === status);
        renderTasks(filtered);
    }
}


// 🌙 DARK MODE
function toggleDark() {
    document.body.classList.toggle("dark");
}


// 🚪 LOGOUT
function logout() {
    localStorage.removeItem("token");
    alert("Logged out");
}