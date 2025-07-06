const apiUrl = 'API_GATEWAY_URL/todos'; // Replace with Terraform output 'api_gateway_url' (e.g., https://abcdef123.execute-api.us-east-1.amazonaws.com/prod/todos)

async function fetchTasks() {
    try {
        const response = await fetch(apiUrl);
        const tasks = await response.json();
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.textContent = `${task.task} ${task.completed ? '(Completed)' : ''}`;
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

async function addTask() {
    const taskInput = document.getElementById('taskInput');
    const task = taskInput.value.trim();
    if (!task) return;

    try {
        await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task })
        });
        taskInput.value = '';
        fetchTasks();
    } catch (error) {
        console.error('Error adding task:', error);
    }
}

// Load tasks on page load
document.addEventListener('DOMContentLoaded', fetchTasks);