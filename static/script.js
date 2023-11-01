
document.getElementById('kandidatSearch').addEventListener('input', function (e) {
    const searchValue = e.target.value;

    // Only search when there are 2 or more characters
    if (searchValue.length >= 2) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/search_name', true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

        xhr.onload = function () {
            if (this.status === 200) {
                const results = JSON.parse(this.responseText);
                updateDropdown(results);
            }
        };

        xhr.send(`name=${searchValue}`);
    } else {
        clearDropdown();
    }
});

// Tooltip scripts

let tooltipTimeout;
let wasClicked = false;

const tooltipIcons = document.querySelectorAll('.tooltip-icon');

function toggleTooltip(tooltipIcon, tooltipContent) {
    if (tooltipContent.style.display === 'none' || !tooltipContent.style.display) {
        clearTimeout(tooltipTimeout);
        tooltipContent.style.display = 'block';
        wasClicked = true;
    } else {
        tooltipContent.style.display = 'none';
        wasClicked = false;
    }
}

tooltipIcons.forEach(function(tooltipIcon) {
    const tooltipContent = tooltipIcon.nextElementSibling;

    tooltipIcon.addEventListener('mouseenter', function() {
        if (!wasClicked) {
            clearTimeout(tooltipTimeout);
            tooltipContent.style.display = 'block';
        }
    });

    tooltipIcon.addEventListener('mouseleave', function() {
        if (!wasClicked) {
            tooltipTimeout = setTimeout(function() {
                tooltipContent.style.display = 'none';
            }, 300);
        }
    });

    tooltipIcon.addEventListener('click', function() {
        toggleTooltip(tooltipIcon, tooltipContent);
    });

    tooltipIcon.addEventListener('touchend', function(e) {
        e.preventDefault();  // Prevent the mouse event from firing
        toggleTooltip(tooltipIcon, tooltipContent);
    });
});




// Loading indicator scripts
document.querySelector('form').addEventListener('submit', function (e) {
    document.getElementById('loadingSpinner').style.display = 'inline-block';
});

window.addEventListener('pageshow', function (event) {
    if (event.persisted) { // true, wenn die Seite aus dem Cache geladen wurde
        document.getElementById('loadingSpinner').style.display = 'none';
    }
});



function updateDropdown(results) {
    const dropdown = document.getElementById('kandidatDropdown');
    clearDropdown();
    results.forEach(person => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        
        a.href = `/detail/${person['kanton_nummer']}/${person['liste_nummer_kanton']}/${person['kandidat_nummer']}`;
        a.textContent = `${person['vorname']} ${person['name']}`;
        
        li.appendChild(a);
        dropdown.appendChild(li);
    });
}


function clearDropdown() {
    const dropdown = document.getElementById('kandidatDropdown');
    while (dropdown.firstChild) {
        dropdown.removeChild(dropdown.firstChild);
    }
}

