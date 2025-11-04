document.addEventListener('DOMContentLoaded', function () {
  const output = document.getElementById('output');
  const okBtn = document.getElementById('okBtn');
  const clearBtn = document.getElementById('clearBtn');

  if (!output || !okBtn || !clearBtn) return;

  // OK button click — fetch from CGI
  okBtn.addEventListener('click', function () {
    fetch('cgi-bin/cgignition.py')
      .then(response => {
        if (!response.ok) throw new Error('Network response not OK: ' + response.status);
        return response.text();
      })
      .then(text => {
        output.innerHTML = text;
      })
      .catch(err => {
        output.textContent = 'Error: ' + err.message;
      });
  });

  // Clear button click
  clearBtn.addEventListener('click', function () {
    output.innerHTML = '';
  });
});
