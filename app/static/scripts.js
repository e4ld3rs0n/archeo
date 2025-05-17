function clearFiles(inputName) {
    const input = document.querySelector(`input[type="file"][name="${inputName}"]`);
    if (input) input.value = '';
}

function append_dropdown(select) {
  if (select.value === "") return;

  // Disable the current dropdown to prevent changes
  select.setAttribute('readonly', true);

  // Create a new dropdown from scratch
  const newDropdown = document.createElement("select");
  newDropdown.name = select.name; // keep same name for backend
  newDropdown.onchange = function() { append_dropdown(this); };

  // Copy options from the original select
  Array.from(select.options).forEach(opt => {
    const option = document.createElement("option");
    option.value = opt.value;
    option.text = opt.text;
    newDropdown.appendChild(option);
  });

  // Set initial value to empty
  newDropdown.value = "";

  // Add to container
  document.getElementById('dynamic-dropdown').appendChild(newDropdown);
}