// Fetch the JSON file
fetch('ai_first.json')
  .then(response => response.json()) // Parse the JSON data
  .then(data => {
    // Loop through the array of students
    data.forEach(student => {
      // Check if the student is old enough to go to college (age >= 18)
      if (student.age >= 18) {
        console.log(`Name: ${student.name}, Age: ${student.age}, Languages: ${student.languages.join(', ')}`);
      }
    });
  })
  .catch(error => console.error('Error fetching the JSON file:', error));
