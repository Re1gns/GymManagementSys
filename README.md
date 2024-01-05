# Gym Management System
The Gym Management System is a software solution designed to streamline and automate various administrative tasks and operations within a fitness center or gym. It typically includes features such as member management, Users to Trainers assignment, User Dashboard, Trainer Dashboard, billing and invoicing, staff (Trainer) management, and reporting. This system aims to enhance the efficiency of gym operations, improve member experience, and provide administrators with tools for better decision-making and organization management.

## Table of Contents

- [Technologies_Used](#technologies-used)
- [Models](#models)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


# Technologies used:

- [Django](#django)
- [HTML](#HTML5)
- [Bootstrap](#Bootstrap5x)
- [JQuery](#jquery)
- [PostgreSQL](#Database)


## Models

## Key Functions of the `models.py` in Django

1. **Define Database Schema:** It defines the structure of the database by specifying the fields, their types, and relationships between different models.

2. **Object-Relational Mapping (ORM):** Django's ORM system allows developers to interact with the database using Python objects rather than writing raw SQL queries. Models serve as the bridge between Python code and the database.

3. **Data Validation:** Models include field types and constraints that enforce data integrity and validation rules. This helps ensure that the data stored in the database meets certain criteria.

4. **Relationships:** Models can establish relationships between different entities, such as one-to-one, one-to-many, or many-to-many relationships. This is essential for organizing and linking data.

5. **CRUD Operations:** The models define methods for creating, retrieving, updating, and deleting records in the database. These operations can be performed using Django's query API.

6. **Administrative Interface:** Django provides an admin interface that allows developers and administrators to manage and manipulate data in the database easily. Models determine what is displayed and how data is edited in the admin interface.

7. **Form Generation:** Models can be used to automatically generate HTML forms for data entry and validation. This simplifies the process of handling user input and storing it in the database.

# There are different classes in the models of this project which includes but not limited to
### Banners Model

- **img**: ImageField for banner images.
- **alt_text**: CharField for alternative text.

### Service Model

- **title**: CharField for the service title.
- **details**: RichTextField for service details.
- **img**: ImageField for service images.


## Features

- **Rich Text Fields**: Utilizes RichTextField for rich text content.
- **Image Uploads**: Handles image uploads using ImageField.
- **User Authentication**: Utilizes Django's User model for subscriber and trainer authentication.
- **Real-time Notifications**: Sends real-time notifications to users and trainers.

## Installation

1. # PostgreSQL Database Installation

Follow these steps to install PostgreSQL on your system.

## Installation Steps

1. **Linux:**

   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib

2. **macOS**

    brew install postgresql

3. **Windows**
    1. **Download:**

   Download the installer from the [official PostgreSQL website](https://www.postgresql.org/download/windows/).

## Additional Information

- Adjust configurations and settings as needed based on your requirements.

- For detailed documentation, visit [PostgreSQL Documentation](https://www.postgresql.org/docs/).
##


## General setup to get you a copy of this project.

1. Clone the repository: `git clone https://github.com/Re1gns/GymManagementSys.git`
2. Create a virtual environment: `python -m venv env` you can replace <"env"> with whatever you like.
3. Activate the virtual environment: `source env/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Database migrations: `python manage.py makemigrations` 
6. Apply database migrations: `python manage.py migrate`

## Usage

1. Run the development server: `python manage.py runserver`
2. Access the project in your browser: `http://localhost:8000`


## Contributing

If you'd like to contribute, please follow the [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [Reigns] - see the [LICENSE](/LICENSE) file for details.
