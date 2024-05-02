/**
 * Copyright (c) 2024, Sebastien Jodogne, ICTEAM UCLouvain, Belgium
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 **/


// Logic for the listing patients page (mainpage.html)
var modal = document.getElementById("filterModal");
var btn = document.getElementById("openFilterModal");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

function closeModal() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function resetFilters() {
  document.getElementById('filterSex').value = ""; // Remet le sexe à 'Any Sex'
  document.getElementById('minAge').value = "";   // Efface le champ âge minimum
  document.getElementById('maxAge').value = "";   // Efface le champ âge maximum

  filterPatients(); // Applique les filtres réinitialisés pour mettre à jour l'affichage
  closeModal();     // Ferme le modal après la réinitialisation
}


function filterPatients() {
  var input = document.getElementById("searchInput").value.toUpperCase();
  var filterSex = document.getElementById("filterSex").value;
  var minAge = parseInt(document.getElementById("minAge").value, 10);
  var maxAge = parseInt(document.getElementById("maxAge").value, 10);

  var table = document.getElementById("patientsTable");
  var tr = table.getElementsByTagName("tr");

  for (var i = 1; i < tr.length; i++) {
      var td = tr[i].getElementsByTagName("td");
      var txtName = td[0].textContent || td[0].innerText;
      var age = parseInt(td[1].textContent || td[1].innerText, 10);
      var sex = td[2].textContent || td[2].innerText.toLowerCase();

      if (
          (txtName.toUpperCase().indexOf(input) > -1 || input === "") &&
          (filterSex === "" || sex === filterSex) &&
          (isNaN(minAge) || age >= minAge) &&
          (isNaN(maxAge) || age <= maxAge)
      ) {
          tr[i].style.display = "";
      } else {
          tr[i].style.display = "none";
      }
  }
}



function addPatient() {
  var name = document.getElementById('newPatientName').value;  // Récupère le nom du nouveau patient
  if (name.trim() === '') {
      alert('Please enter a name.');
      return;
  }

  var newPatient = {
      id: patients.length + 1,  // Attribue un ID simple basé sur la longueur du tableau
      name: name,
      details: 'Details will be added later'  // Mettez ici des détails par défaut ou supplémentaires
  };

  // Ajoute à la liste des patients
  patients.push(newPatient);

  // Ajoute au tableau HTML
  var table = document.getElementById('patientsTable').getElementsByTagName('tbody')[0];
  var row = table.insertRow();
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  cell1.innerHTML = newPatient.name;
  cell2.innerHTML = '<a href="specificpage.html?patientId=' + newPatient.id + '">See more</a>';

  // Réinitialise le champ de saisie
  document.getElementById('newPatientName').value = '';
}

// End of the code for the listing patients page (mainpage.html)
//-------------------------------------------------------------------------------------------------------------------

// Logic for the specific patient page (specificpage.html)


// Fetch data for the specific patient, display it, handle user interactions, etc.

// Select the <ul> element representing the death wish list
const deathWishList = document.getElementById('deathwishes');

// TODO: REPLACE FAKE DATA WITH DATA FROM DB!
const deathWishesData = ["Travel to Paris", "Write a letter to grandson", "See family from abroad"];

// Clear existing death wish list items
deathWishList.innerHTML = '';

// Populate the death wish list with new items
deathWishesData.forEach(wish => {const listItem = document.createElement('li');
listItem.textContent = wish; 
deathWishList.appendChild(listItem);});

calculateAge(new Date(1990, 1, 1));



// Calculate the age for the specific page from the birthdate and the current date
function calculateAge(birthdate) {
  const age = new Date().getFullYear() - birthdate.getFullYear();
  // Set the age in the HTML (id called age)
  document.getElementById('age').textContent = age;
}



// End of the code for the specific patient page (specificpage.html)
// -------------------------------------------------------------------------------------------------------------------

// Code from Sebastian TP session


// function refreshTemperatures() {
//   var select = document.getElementById('patient-select');
//   var id = select.value;
//   if (id === '') {
//     console.log('No patient');
//     document.getElementById('temperature-div').style.visibility = 'hidden';
//     return;
//   }

//   document.getElementById('temperature-div').style.visibility = 'visible';

//   axios.get('temperatures', {
//     params: {
//       id: id
//     },
//     responseType: 'json'
//   })
//     .then(function(response) {
//       var x = [];
//       var y = [];
//       for (var i = 0; i < response.data.length; i++) {
//         x.push(response.data[i]['time']);
//         y.push(response.data[i]['temperature']);
//       }
//       chart.data.labels = x;
//       chart.data.datasets[0].data = y;
//       chart.update();
//     })
//     .catch(function(response) {
//       alert('URI /temperatures not properly implemented in Flask');
//     });
// }


// function refreshPatients() {
//   axios.get('patients', {
//     responseType: 'json'
//   })
//     .then(function(response) {
//       var select = document.getElementById('patient-select');

//       while (select.options.length > 0) {
//         select.options.remove(0);
//       }

//       for (var i = 0; i < response.data.length; i++) {
//         var id = response.data[i]['id'];
//         var name = response.data[i]['name'];
//         select.appendChild(new Option(name, id));
//       }
//       refreshTemperatures();
//     })
//     .catch(function(response) {
//       alert('URI /patients not properly implemented in Flask');
//     });
// }


// document.addEventListener('DOMContentLoaded', function() {
//   chart = new Chart(document.getElementById('temperatures'), {
//     type: 'line',
//     data: {
//       labels: [],
//       datasets: [{
//         label: 'Temperature',
//         data: [],
//         fill: false
//       }]
//     },
//     options: {
//       animation: {
//         duration: 0  // Disable animations
//       },
//       scales: {
//         x: {
//           ticks: {
//             // Rotate the X label
//             maxRotation: 45,
//             minRotation: 45
//           }
//         }
//       }
//     }
//   });

//   refreshPatients();

//   document.getElementById('patient-select').addEventListener('change', refreshTemperatures);

//   document.getElementById('patient-button').addEventListener('click', function() {
//     var name = document.getElementById('patient-input').value;
//     if (name == '') {
//       alert('No name was provided');
//     } else {
//       axios.post('create-patient', {
//         name: name
//       })
//         .then(function(response) {
//           document.getElementById('patient-input').value = '';
//           refreshPatients();
//         })
//         .catch(function(response) {
//           alert('URI /create-patient not properly implemented in Flask');
//         });
//     }
//   });

//   document.getElementById('temperature-button').addEventListener('click', function() {
//     var temperature = parseFloat(document.getElementById('temperature-input').value);
//     if (isNaN(temperature)) {
//       alert('Not a valid number');
//     } else {
//       axios.post('record', {
//         id: document.getElementById('patient-select').value,
//         temperature: temperature
//       })
//         .then(function(response) {
//           document.getElementById('temperature-input').value = '';
//           refreshTemperatures();
//         })
//         .catch(function(response) {
//           alert('URI /record not properly implemented in Flask');
//         });
//     }
//   });
// });
