# Task Management Dashboard (Tasky)

Task Management Dashboard is a web application built using Django, allowing users to manage tasks with features like task creation, status updates, drag-and-drop functionality, and search capabilities.

## Features

- **Task Management**: Create, update, and delete tasks with different statuses (In Progress, Completed, Overdue).
- **Drag-and-Drop**: Sort tasks using drag-and-drop functionality for easy task management.
- **Search**: Search tasks based on title and other criteria.
- **Responsive Design**: UI optimized for desktop and mobile devices.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript (jQuery, SortableJS)
- **Database**: SQLite (for development)
- **Other Tools**: Django REST Framework (for API development), AJAX for asynchronous updates

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dee-engineer/tasky.git
   cd task-management-dashboard

2. Install Requirements:

   ```bash
   pip install -r requirements.txt

3. Run Migration:

   ```bash
   python manage.py migrate

4. Run Server:

   ```bash
   python manage.py runserver

Default Login:
   - username: divine
   - password: dee


Usage
    Task Management: Navigate through different task categories (In Progress, Completed, Overdue). Use the drag-and-drop feature to change task statuses.
    Search: Use the search bar to find tasks by title or other criteria.
    Task Actions: Click on task action icons (Edit, Delete) to perform respective actions.
    Responsive Design: Access and manage tasks seamlessly on both desktop and mobile devices.